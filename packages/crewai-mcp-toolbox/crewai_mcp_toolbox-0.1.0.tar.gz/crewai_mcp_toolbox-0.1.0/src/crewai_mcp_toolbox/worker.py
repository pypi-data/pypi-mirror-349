"""Worker thread for managing MCP server processes.

This module provides the MCPWorkerThread class, which handles:
- Starting and stopping an MCP server process
- Establishing and maintaining communication with the server
- Discovering available tools
- Executing tool calls in a thread-safe manner
"""

import asyncio
import concurrent.futures
import logging
import queue
import threading
import time
import uuid
from contextlib import AsyncExitStack
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, cast

# Configure logging
logger = logging.getLogger(__name__)

# Type definitions for type checking
if TYPE_CHECKING:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.types import Tool as MCPTool

# Try to import the real MCP library
try:
    import mcp
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    from mcp.types import Tool as MCPTool

    MCP_AVAILABLE = True
    logger.debug("MCP library successfully imported.")
except ImportError:
    logger.warning("MCP library not found. Using stub implementations.")
    MCP_AVAILABLE = False

    # Define stubs for runtime when MCP isn't available
    # Note: TYPE_CHECKING is False at runtime, so this condition is always True here
    class ClientSession:
        """Stub ClientSession implementation."""

        pass

    class StdioServerParameters:
        """Stub StdioServerParameters implementation."""

        pass

    stdio_client = Any

    class MCPTool:
        """Stub implementation when real MCP isn't available"""

        def __init__(self, name="stub_tool", description="Stub tool"):
            self.name = name
            self.description = description
            self.inputSchema = {}


# Import this after the type definitions to avoid circular imports
from .exceptions import MCPToolExecutionError
from .utils import MCPConfiguration


# Add these after importing MCPToolExecutionError
class MCPConnectionError(MCPToolExecutionError):
    """Exception raised when there is an error in MCP connection or communication."""

    pass


class MCPProcessError(MCPToolExecutionError):
    """Exception raised when the MCP server process fails."""

    pass


class MCPWorkerThread:
    """Manages a dedicated thread for asynchronous communication with an MCP server."""

    def __init__(
        self,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the MCP worker thread.

        Args:
            command: The command to start the MCP server.
            args: Arguments for the command.
            env: Optional environment variables for the process.
            config: Optional configuration for the worker.
        """
        self._command = command
        self._args = args
        self._env = env
        self._config = MCPConfiguration(config)
        self._request_queue: queue.Queue[
            Optional[Tuple[str, str, Dict[str, Any]]]
        ] = queue.Queue()
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._connection: Optional[ClientSession] = None
        self._tools: List["MCPTool"] = []
        self._pending_futures: Dict[str, concurrent.futures.Future] = {}
        self._lock = threading.Lock()
        self._startup_complete = threading.Event()
        self._startup_success: Optional[bool] = None
        self._shutdown_requested = threading.Event()
        self._startup_lock = threading.Lock()
        self._tools_lock = threading.Lock()

        # Attributes for process management
        self._process = (
            None  # Will store a reference to the subprocess when available
        )
        self._startup_error: Optional[Exception] = (
            None  # Store the specific startup error
        )
        self._process_healthy = threading.Event()
        self._process_healthy.set()  # Assume healthy to start
        self._health_check_interval = self._config.get(
            "health_check_interval", 10.0
        )  # seconds
        self._health_check_task = None

        # Display warning if MCP is not available
        if not MCP_AVAILABLE:
            logger.warning(
                "MCP library not available. Limited functionality will be available."
            )

    def is_alive(self) -> bool:
        """Checks if the worker thread is currently running."""
        return self._thread is not None and self._thread.is_alive()

    def get_tools(self, force_refresh: bool = False) -> List["MCPTool"]:
        """Returns the list of discovered MCP tools with thread safety.

        Args:
            force_refresh: If True, queries the server for the latest tools list.
                           If False (default), uses the cached tools list.

        Returns:
            A copy of the current list of discovered MCP tools.

        Raises:
            RuntimeError: If the worker thread is not running, not ready, or failed
                          during startup.
        """
        if not self.is_alive():
            raise RuntimeError("MCP Worker thread not started.")

        if not self._startup_complete.is_set():
            # Wait briefly in case startup is imminent, but don't block indefinitely
            if not self._startup_complete.wait(timeout=0.1):
                raise RuntimeError("MCP Worker thread not ready.")

        with self._startup_lock:
            if not self._startup_success:
                raise RuntimeError("MCP Worker thread failed during startup.")

        if force_refresh and self._connection:
            self._refresh_tools()

        # Return a consistent snapshot of the tools list
        with self._tools_lock:
            # Return a copy to prevent modification by the caller
            return list(self._tools)

    def _refresh_tools(self) -> None:
        """Request a refresh of the tools list from the worker thread.

        This method handles the thread-safe refresh mechanism by submitting
        the refresh task to the worker's event loop.
        """
        # Use a thread-safe mechanism to request refresh from the worker loop
        refresh_complete = threading.Event()
        refresh_error: List[Optional[Exception]] = [None]

        async def do_refresh() -> None:
            """Async function executed in the worker's event loop."""
            try:
                if not self._connection:
                    raise RuntimeError(
                        "No MCP connection available for refresh"
                    )
                response = await self._connection.list_tools()
                with self._tools_lock:
                    self._tools = response.tools
                logger.info(
                    f"Refreshed MCP tools list: found {len(self._tools)} tools"
                )
            except Exception as e:
                logger.error(
                    f"Error refreshing tools list: {e}", exc_info=True
                )
                refresh_error[0] = e
            finally:
                refresh_complete.set()

        if self._loop and self._loop.is_running():
            try:
                future = asyncio.run_coroutine_threadsafe(
                    do_refresh(), self._loop
                )
                # Wait for the refresh operation to complete in the worker thread
                future.result(timeout=10.0)  # Wait up to 10 seconds
                if refresh_error[0]:
                    # Log the error but don't raise, return potentially stale data
                    logger.warning(
                        "Tool refresh completed with error: %s",
                        refresh_error[0],
                    )
            except concurrent.futures.TimeoutError:
                logger.warning("Tool refresh operation timed out after 10s")
            except Exception as e:
                logger.error(
                    f"Failed to schedule or execute tool refresh: {e}",
                    exc_info=True,
                )
        else:
            logger.warning(
                "Cannot refresh tools: Worker event loop not running"
            )

    def start(self) -> None:
        """Starts the worker thread and initializes the MCP connection.

        Waits for the worker thread to signal successful startup, including
        establishing the connection and fetching the initial tool list.

        Raises:
            TimeoutError: If the worker thread fails to start within the timeout.
            RuntimeError: If the worker thread fails during the startup sequence.
        """
        if self.is_alive():
            logger.debug("MCP Worker thread already running.")
            return

        # Reset state
        logger.info("Starting MCP Worker thread...")
        self._shutdown_requested.clear()
        self._startup_complete.clear()
        self._startup_success = None
        self._startup_error = None
        self._pending_futures.clear()
        self._process_healthy.set()

        self._thread = threading.Thread(
            target=self._run_worker, daemon=True, name="MCPWorkerThread"
        )
        self._thread.start()

        # Wait for startup signal from the worker thread
        startup_timeout = self._config.worker_startup_timeout
        logger.debug(
            f"Waiting up to {startup_timeout}s for MCP worker startup..."
        )
        if not self._startup_complete.wait(timeout=startup_timeout):
            logger.error("MCP Worker thread startup timed out.")
            self._request_shutdown()  # Attempt cleanup
            raise TimeoutError(
                f"MCP Worker thread failed to start up within {startup_timeout} seconds."
            )

        with self._startup_lock:
            if not self._startup_success:
                error_msg = (
                    str(self._startup_error)
                    if self._startup_error
                    else "Unknown error"
                )
                logger.error(
                    f"MCP Worker thread failed during startup sequence: {error_msg}"
                )
                raise RuntimeError(
                    f"MCP Worker thread failed during startup: {error_msg}"
                )

        logger.info(
            "MCP Worker thread started and connection initialized successfully."
        )

    def _force_terminate_process(self) -> None:
        """Forcefully terminate the MCP server process if it's running."""
        if not self._process:
            return

        try:
            if hasattr(self._process, "poll") and self._process.poll() is None:
                logger.warning("Forcefully terminating MCP server process...")

                # Try graceful termination first
                try:
                    self._process.terminate()

                    # Give it a moment to terminate
                    for _ in range(5):
                        if self._process.poll() is not None:
                            logger.info(
                                "MCP server process terminated gracefully"
                            )
                            break
                        time.sleep(0.1)

                    # If still running, force kill
                    if self._process.poll() is None:
                        logger.warning(
                            "MCP server not responding to terminate, using kill signal"
                        )
                        if hasattr(self._process, "kill"):
                            self._process.kill()
                            self._process.wait(1.0)
                            logger.info("MCP server process forcefully killed")

                except Exception as e:
                    logger.error(
                        f"Error terminating MCP server process: {e}",
                        exc_info=True,
                    )
        except Exception as e:
            logger.error(
                f"Unexpected error in process termination: {e}", exc_info=True
            )

    def stop(self) -> None:
        """Signals the worker thread to shut down and waits for it to exit.

        Attempts a graceful shutdown first, then performs cleanup if the
        thread does not exit cleanly within a timeout.
        """
        if not self.is_alive():
            logger.debug("MCP Worker thread already stopped.")
            return

        logger.info("Stopping MCP Worker thread...")
        self._request_shutdown()

        if self._thread:
            join_timeout = 10.0
            self._thread.join(timeout=join_timeout)

            if self._thread.is_alive():
                logger.warning(
                    f"MCP Worker thread did not exit cleanly after {join_timeout}s. "
                    "Force cleanup may be incomplete."
                )
                # Force terminate the subprocess if it's still running
                self._force_terminate_process()
                # Clear resources
                self._connection = None
                with self._tools_lock:
                    self._tools = []
                self._fail_all_pending(RuntimeError("Forced worker shutdown"))
            else:
                logger.debug("MCP Worker thread joined successfully.")

        self._thread = None
        logger.info("MCP Worker thread stop procedure completed.")

    def _request_shutdown(self) -> None:
        """Internal method to signal shutdown and clean pending futures."""
        if self._shutdown_requested.is_set():
            return

        logger.debug("Signaling MCP worker shutdown...")
        self._shutdown_requested.set()
        # Unblock queue.get() in the worker loop
        self._request_queue.put(None)
        # Cancel any pending futures immediately
        self._fail_all_pending(RuntimeError("MCP Worker shutting down"))

    def submit_request(
        self, tool_name: str, args: Dict[str, Any]
    ) -> concurrent.futures.Future:
        """Submits a tool call request to the worker thread.

        Args:
            tool_name: The name of the tool to call.
            args: The arguments for the tool call.

        Returns:
            A Future object that will contain the result of the tool call.
        """
        future = concurrent.futures.Future()

        with self._lock:
            if not self.is_alive():
                future.set_exception(
                    RuntimeError("MCP Worker thread is not running")
                )
                return future

            if not self._startup_complete.is_set():
                future.set_exception(
                    RuntimeError("MCP Worker thread is not ready")
                )
                return future

            # Check process health
            if not self._process_healthy.is_set():
                future.set_exception(
                    MCPConnectionError("MCP server process is not healthy")
                )
                return future

            # Generate a unique ID for the request
            req_id = uuid.uuid4().hex
            self._pending_futures[req_id] = future

            try:
                # Add request to the queue for the worker thread to process
                self._request_queue.put((req_id, tool_name, args))
                logger.debug(
                    f"Submitted request {req_id} for tool '{tool_name}'"
                )
            except Exception as e:
                # If queueing fails, remove the future and raise
                self._pending_futures.pop(req_id, None)
                future.set_exception(e)
                logger.error(
                    f"Failed to queue request for tool '{tool_name}': {e}"
                )

        return future

    def _run_worker(self) -> None:
        """The main function executed by the worker thread.

        Sets up the asyncio event loop and runs the async worker logic.
        Handles exceptions and ensures cleanup.
        """
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            logger.debug(
                f"MCP Worker thread {threading.get_ident()} starting event loop."
            )
            self._loop.run_until_complete(self._async_worker())
        except asyncio.CancelledError:
            logger.info("MCP Worker thread async task cancelled.")
            with self._startup_lock:
                if self._startup_success is None:
                    self._startup_success = False
        except Exception as e:
            logger.exception(
                f"MCP Worker thread encountered an unhandled exception: {e}"
            )
            with self._startup_lock:
                if self._startup_success is None:
                    self._startup_success = False
        finally:
            # Ensure startup_success is set if it wasn't already
            with self._startup_lock:
                if self._startup_success is None:
                    logger.warning(
                        "Worker terminated before startup completed."
                    )
                    self._startup_success = False
                    if not self._startup_error:
                        self._startup_error = RuntimeError(
                            "Worker terminated before startup completed"
                        )

            # Fail any futures that were still pending
            self._fail_all_pending(
                RuntimeError("MCP Worker thread terminated unexpectedly")
            )

            # Forcefully terminate the process if needed
            self._force_terminate_process()

            # Clean up the event loop
            if self._loop:
                self._cleanup_event_loop()

            # Ensure the startup event is set to unblock the main thread
            if not self._startup_complete.is_set():
                logger.debug(
                    "Setting startup_complete event (worker exiting)."
                )
                self._startup_complete.set()

            logger.info(f"MCP Worker thread {threading.get_ident()} finished.")

    def _cleanup_event_loop(self) -> None:
        """Clean up the asyncio event loop safely."""
        try:
            if self._loop and self._loop.is_running():
                logger.debug("Stopping worker event loop...")
                self._loop.call_soon_threadsafe(self._loop.stop)
                # Give loop time to process stop signal
                time.sleep(0.1)

            if self._loop:
                logger.debug("Closing worker event loop...")
                self._loop.close()
                logger.debug("Worker event loop closed.")
        except Exception as loop_close_exc:
            logger.error(
                f"Error closing worker event loop: {loop_close_exc}",
                exc_info=True,
            )
        self._loop = None

    async def _check_process_health(self) -> bool:
        """Check if the MCP server process is healthy.

        Returns:
            bool: True if the process is healthy, False otherwise.
        """
        # If we don't have a connection or process, we can't check health
        if not self._connection:
            return False

        try:
            # Simple connectivity check with a short timeout
            await asyncio.wait_for(self._connection.list_tools(), timeout=2.0)
            return True
        except (asyncio.TimeoutError, ConnectionError, Exception) as e:
            logger.warning(f"MCP server health check failed: {e}")
            return False

    async def _periodic_health_check(self) -> None:
        """Periodically check the health of the MCP server process."""
        logger.debug(
            f"Starting health check task (interval: {self._health_check_interval}s)"
        )

        while not self._shutdown_requested.is_set():
            try:
                if self._connection:
                    is_healthy = await self._check_process_health()

                    # Only update state when there's a change
                    if not is_healthy and self._process_healthy.is_set():
                        logger.warning("MCP server process is not healthy")
                        self._process_healthy.clear()
                    elif is_healthy and not self._process_healthy.is_set():
                        logger.info("MCP server process is now healthy")
                        self._process_healthy.set()

                # Wait for the next check interval
                await asyncio.sleep(self._health_check_interval)

            except Exception as e:
                logger.error(f"Error in health check task: {e}", exc_info=True)
                await asyncio.sleep(
                    1.0
                )  # Short delay before retrying on error

        logger.debug("Health check task exiting")

    async def _async_worker(self) -> None:
        """Contains the asynchronous logic run within the worker's event loop.

        Establishes the MCP connection, lists initial tools, and processes
        requests from the queue until shutdown is requested.
        """
        logger.debug("MCP async worker started.")
        exit_stack = AsyncExitStack()
        try:
            if not MCP_AVAILABLE:
                await self._handle_mcp_unavailable()
                return

            # Initialize MCP Connection via stdio
            await self._initialize_mcp_connection(exit_stack)

            # Signal successful startup
            with self._startup_lock:
                self._startup_success = True
            self._startup_complete.set()
            logger.debug("MCP worker signaled successful startup.")

            # Main request processing loop
            await self._process_requests_loop()

        except Exception as init_exc:
            logger.exception(
                f"MCP worker failed during initialization: {init_exc}"
            )
            with self._startup_lock:
                self._startup_success = False
            if not self._startup_complete.is_set():
                self._startup_complete.set()
            self._fail_all_pending(init_exc)

        finally:
            await self._cleanup_async_resources(exit_stack)

    async def _handle_mcp_unavailable(self) -> None:
        """Handle the case where MCP is not available."""
        with self._tools_lock:
            # Create a stub tool for testing
            self._tools = [MCPTool(name="stub_tool", description="Stub tool")]
        logger.info("Using stub tools as MCP is not available")

        # Signal successful startup with limited functionality
        with self._startup_lock:
            self._startup_success = True
            self._startup_error = None  # Clear any startup error
        self._startup_complete.set()
        logger.debug("MCP worker signaled successful startup.")

        # Start health check task
        self._health_check_task = asyncio.create_task(
            self._periodic_health_check()
        )

        # Just wait until shutdown is requested
        while not self._shutdown_requested.is_set():
            await asyncio.sleep(0.1)

    async def _initialize_mcp_connection(
        self, exit_stack: AsyncExitStack
    ) -> None:
        """Initialize the MCP connection.

        Args:
            exit_stack: The AsyncExitStack to register the connection with.
        """
        logger.debug(
            f"Initializing MCP connection: cmd='{self._command}', args={self._args}"
        )
        server_params = StdioServerParameters(
            command=self._command, args=self._args, env=self._env
        )
        stdio_transport = await exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        stdio, write = stdio_transport
        await self._store_process_reference(stdio_transport)
        logger.debug("MCP stdio transport established in worker.")

        self._connection = await exit_stack.enter_async_context(
            ClientSession(stdio, write)
        )
        await self._connection.initialize()
        logger.debug("MCP ClientSession initialized in worker.")

        # Fetch initial list of tools
        response = await self._connection.list_tools()
        with self._tools_lock:
            self._tools = response.tools
        logger.info(
            f"MCP worker discovered tools: {[t.name for t in self._tools]}"
        )

        # Start health check task
        self._health_check_task = asyncio.create_task(
            self._periodic_health_check()
        )

    async def _store_process_reference(self, stdio_transport: Any) -> None:
        """Store a reference to the MCP server process.

        Args:
            stdio_transport: The stdio transport from which to get the process.
        """
        try:
            if hasattr(stdio_transport, "_process"):
                self._process = stdio_transport._process
                if self._process:
                    pid = getattr(self._process, "pid", "unknown")
                    logger.debug(
                        f"Stored reference to MCP server process (pid: {pid})"
                    )
            elif hasattr(stdio_transport, "_transport") and hasattr(
                stdio_transport._transport, "_process"
            ):
                self._process = stdio_transport._transport._process
                if self._process:
                    pid = getattr(self._process, "pid", "unknown")
                    logger.debug(
                        f"Stored reference to MCP server process from transport (pid: {pid})"
                    )
        except Exception as e:
            logger.warning(f"Unable to store reference to MCP process: {e}")

    async def _process_requests_loop(self) -> None:
        """Process requests from the queue until shutdown is requested."""
        while not self._shutdown_requested.is_set():
            try:
                # Use run_in_executor for the blocking queue.get()
                request = await self._loop.run_in_executor(
                    None, self._request_queue.get
                )

                if request is None:  # Sentinel value for shutdown
                    logger.debug("MCP worker received shutdown sentinel.")
                    break

                if self._shutdown_requested.is_set():
                    logger.debug("Shutdown requested while waiting for task.")
                    # Fail the request that was just dequeued during shutdown
                    req_id, _, _ = request
                    self._fail_pending_future(
                        req_id, RuntimeError("MCP Worker shutting down")
                    )
                    break

                req_id, tool_name, args = request
                logger.debug(
                    f"MCP worker processing request {req_id} for tool '{tool_name}'"
                )

                # Schedule tool execution as a background task
                asyncio.create_task(
                    self._execute_tool_and_respond(req_id, tool_name, args)
                )

            except queue.Empty:
                # Should not happen with blocking get, but handle defensively
                await asyncio.sleep(0.01)
                continue
            except Exception as loop_exc:
                logger.error(
                    f"Error in MCP worker processing loop: {loop_exc}",
                    exc_info=True,
                )
                # If associated with a specific request, fail its future
                if "req_id" in locals():
                    self._fail_pending_future(req_id, loop_exc)
                await asyncio.sleep(0.1)  # Avoid busy-looping

    async def _cleanup_async_resources(
        self, exit_stack: AsyncExitStack
    ) -> None:
        """Clean up async resources.

        Args:
            exit_stack: The AsyncExitStack to close.
        """
        logger.debug("MCP async worker cleaning up resources...")

        # Cancel the health check task if it's running
        if self._health_check_task and not self._health_check_task.done():
            logger.debug("Cancelling health check task")
            self._health_check_task.cancel()
            try:
                # Give it a chance to clean up
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                pass

        # Continue with normal cleanup
        await exit_stack.aclose()  # Ensures connection cleanup
        self._connection = None
        logger.debug("MCP async worker resource cleanup complete.")

    async def _execute_tool_and_respond(
        self, req_id: str, tool_name: str, args: Dict[str, Any]
    ) -> None:
        """Executes the MCP tool call and sets the result or exception on the future.

        Args:
            req_id: The unique ID of the request.
            tool_name: The name of the tool to call.
            args: The arguments for the tool call.
        """
        # Get the future outside the lock to avoid holding the lock during the call
        future = self._get_future(req_id)
        if not future:
            return

        try:
            logger.debug(
                f"Executing MCP tool '{tool_name}' for request {req_id}"
            )

            if not MCP_AVAILABLE:
                await self._handle_stub_tool_execution(future, tool_name, args)
                return

            if not self._connection:
                raise RuntimeError(
                    f"MCP connection lost before executing tool '{tool_name}'"
                )

            await self._execute_real_tool(future, req_id, tool_name, args)

        except Exception as e:
            # Catch exceptions in the surrounding logic (e.g., connection issues)
            logger.error(
                f"Unexpected error during execution/response for request {req_id} ('{tool_name}'): {e}",
                exc_info=True,
            )
            if future and not future.done():
                future.set_exception(e)
        finally:
            # Defensive check: ensure future is removed if error occurred before pop
            self._cleanup_stale_future(req_id)

    def _get_future(self, req_id: str) -> Optional[concurrent.futures.Future]:
        """Get and remove the future for a request.

        Args:
            req_id: The ID of the request.

        Returns:
            The future for the request, or None if not found or already done.
        """
        with self._lock:
            # Retrieve and remove the future atomically
            future = self._pending_futures.pop(req_id, None)

        if future is None:
            logger.warning(
                f"Future for request {req_id} not found. "
                "Request might have been cancelled or already completed."
            )
            return None

        if future.done():
            logger.warning(f"Future for request {req_id} was already done.")
            return None

        return future

    async def _handle_stub_tool_execution(
        self,
        future: concurrent.futures.Future,
        tool_name: str,
        args: Dict[str, Any],
    ) -> None:
        """Handle execution for stub tools when MCP is not available.

        Args:
            future: The future to set the result on.
            tool_name: The name of the tool to call.
            args: The arguments for the tool call.
        """
        logger.debug(f"Using stub implementation for tool '{tool_name}'")

        # Create a simple response that mimics MCP tool output
        if tool_name == "stub_tool":
            # Default stub tool
            result = f"Stub result for tool '{tool_name}' with args: {args}"
        else:
            # Handle unknown tools
            result = (
                f"Stub response: Tool '{tool_name}' called with args: {args}"
            )

        future.set_result(result)

    async def _execute_real_tool(
        self,
        future: concurrent.futures.Future,
        req_id: str,
        tool_name: str,
        args: Dict[str, Any],
    ) -> None:
        """Execute a real MCP tool call.

        Args:
            future: The future to set the result on.
            req_id: The unique ID of the request.
            tool_name: The name of the tool to call.
            args: The arguments for the tool call.
        """
        # Apply a timeout to the individual MCP tool call
        per_call_timeout = self._config.per_call_timeout
        try:
            result = await asyncio.wait_for(
                self._connection.call_tool(tool_name, args),
                timeout=per_call_timeout,
            )
            logger.debug(
                f"MCP tool '{tool_name}' (req {req_id}) completed successfully."
            )

            future.set_result(result)

        except asyncio.TimeoutError:
            error_msg = f"MCP tool '{tool_name}' call timed out after {per_call_timeout}s"
            logger.error(error_msg)
            future.set_exception(TimeoutError(error_msg))
        except Exception as tool_call_exc:
            # Catch exceptions specifically from call_tool
            logger.error(
                f"Error calling MCP tool '{tool_name}' for request {req_id}: {tool_call_exc}",
                exc_info=True,
            )
            wrapped_exc = MCPToolExecutionError(
                f"Error calling MCP tool '{tool_name}'"
            )
            wrapped_exc.__cause__ = tool_call_exc
            future.set_exception(wrapped_exc)

    def _cleanup_stale_future(self, req_id: str) -> None:
        """Clean up any stale futures that might still be in the pending dict.

        Args:
            req_id: The ID of the request to check for.
        """
        with self._lock:
            if req_id in self._pending_futures:
                logger.warning(
                    f"Future {req_id} was not removed during processing, removing now."
                )
                stale_future = self._pending_futures.pop(req_id)
                if not stale_future.done():
                    stale_future.set_exception(
                        RuntimeError("Future processing error")
                    )

    def _fail_pending_future(self, req_id: str, exception: Exception) -> None:
        """Safely sets an exception on a specific pending future.

        Args:
            req_id: The ID of the request whose future should be failed.
            exception: The exception instance to set on the future.
        """
        # Get and remove the future under the lock
        future = None
        with self._lock:
            future = self._pending_futures.pop(req_id, None)

        # Set the exception outside the lock to avoid potential deadlocks
        if future and not future.done():
            logger.warning(
                f"Failing future {req_id} due to error: {exception}"
            )
            future.set_exception(exception)

    def _fail_all_pending(self, exception: Exception) -> None:
        """Sets an exception on all currently pending futures.

        Used during shutdown or catastrophic failure.

        Args:
            exception: The exception instance to set on all pending futures.
        """
        # Get a snapshot of pending futures under the lock
        futures_to_fail = []
        with self._lock:
            if not self._pending_futures:
                return

            num_pending = len(self._pending_futures)
            logger.warning(
                f"Failing all {num_pending} pending MCP requests due to: {exception}"
            )

            # Make a copy of the items for safe processing outside the lock
            for req_id, future in list(self._pending_futures.items()):
                if not future.done():
                    futures_to_fail.append((req_id, future))
            self._pending_futures.clear()

        # Set exceptions outside the lock
        for req_id, future in futures_to_fail:
            future.set_exception(exception)

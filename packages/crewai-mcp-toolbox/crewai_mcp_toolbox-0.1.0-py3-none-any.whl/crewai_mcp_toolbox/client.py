"""Client for interacting with MCP servers from CrewAI agents.

This module provides the MCPToolSet class, which manages the lifecycle of an
MCP server and exposes its tools as CrewAI-compatible tools.
"""

import concurrent.futures
import logging
import os
from typing import Any, Dict, List, Optional

from crewai.tools import BaseTool

from .factory import MCPToolFactory
from .utils import MCPConfiguration, process_mcp_result
from .worker import MCPWorkerThread

# Configure logging
logger = logging.getLogger(__name__)


class MCPToolSet:
    """Manages the lifecycle of an MCP server process and associated CrewAI tools.

    Acts as a context manager to ensure the MCP server process (managed by
    MCPWorkerThread) is started and stopped correctly. Discovers tools from the
    server upon initialization and provides them as a list of CrewAI BaseTool objects.

    Usage:
        # Using a directory-based filesystem server
        async with MCPToolSet(directory_path="./mcp_data") as tools:
            agent = Agent(tools=tools, ...)
            agent.kickoff()

        # Using a custom command
        async with MCPToolSet(command="uvx", args=["my-mcp-server"]) as tools:
            agent = Agent(tools=tools, ...)
            agent.kickoff()

    Attributes:
        tools: A list of initialized CrewAI BaseTool objects representing the
               tools discovered from the MCP server.
        _worker: The MCPWorkerThread instance managing the server process
                 and communication.
    """

    def __init__(
        self,
        directory_path: Optional[str] = None,
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        env: Optional[Dict[str, str]] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initializes the MCPToolSet configuration.

        Determines the command and arguments needed to start the MCP server,
        either via a specified directory (using npx server-filesystem) or
        a custom command.

        Args:
            directory_path: Path to a directory for a filesystem MCP server.
                            If provided, `command` and `args` are ignored.
            command: The command to run the MCP server (e.g., 'python', 'npx').
                     Required if `directory_path` is not provided.
            args: A list of arguments for the command.
            env: Optional environment variables for the server process.
            config: Optional configuration dictionary with the following keys:
                - worker_startup_timeout: Seconds to wait for worker thread startup (default: 60.0)
                - tool_execution_timeout: Seconds to wait for tool execution (default: 90.0)
                - batch_execution_timeout: Seconds to wait for batch operations (default: 180.0)
                - per_call_timeout: Seconds to wait for individual MCP calls (default: 60.0)

        Raises:
            ValueError: If neither `directory_path` nor `command` is provided,
                        or if `directory_path` is provided along with `command`.
        """
        if directory_path and command:
            raise ValueError(
                "Specify either 'directory_path' or 'command', not both."
            )
        if not directory_path and not command:
            raise ValueError(
                "Must provide either 'directory_path' or 'command'."
            )

        # Initialize configuration
        self._config = MCPConfiguration(config)

        final_command: str
        final_args: List[str]

        if directory_path:
            # Configure for npx filesystem server
            final_command = "npx"
            abs_path = os.path.abspath(directory_path)
            os.makedirs(abs_path, exist_ok=True)
            final_args = [
                "-y",  # Auto-install package if needed
                "@modelcontextprotocol/server-filesystem",
                abs_path,
            ]
            logger.info(
                f"MCPToolSet configured for filesystem server at: {abs_path}"
            )
        else:
            # Configure for custom command
            final_command = command  # type: ignore[assignment] # Checked above
            final_args = args if args is not None else []
            logger.info(
                f"MCPToolSet configured with command='{final_command}', args={final_args}"
            )

        # Create the worker but delay starting it until initialization/context entry
        self._worker = MCPWorkerThread(
            command=final_command, args=final_args, env=env, config=config
        )
        self.tools: List[BaseTool] = []

    def initialize(self) -> List[BaseTool]:
        """Starts the MCP worker thread, discovers tools, and creates CrewAI tools.

        This method is called automatically when entering the context manager.
        It can also be called manually if not using the context manager pattern,
        but cleanup() must be called separately in that case.

        Returns:
            A list of initialized CrewAI BaseTool objects.

        Raises:
            RuntimeError: If the worker fails to start or tool creation fails.
            TimeoutError: If the worker startup times out.
        """
        if self._worker.is_alive() and self.tools:
            logger.debug(
                "MCP worker already running and tools initialized. Returning cached tools."
            )
            return self.tools

        logger.info(
            "Initializing MCPToolSet: Starting worker and discovering tools..."
        )
        try:
            # Start worker (handles connection, initial tool list, and startup wait)
            self._worker.start()
        except (RuntimeError, TimeoutError) as start_err:
            logger.error(f"Failed to start MCP worker: {start_err}")
            self.cleanup()  # Ensure cleanup attempt on failed start
            raise start_err

        # Worker started successfully, now retrieve the discovered MCP tool definitions
        try:
            mcp_tools = self._worker.get_tools()
        except RuntimeError as get_tools_err:
            logger.error(
                f"Failed to get tools from successfully started worker: {get_tools_err}"
            )
            self.cleanup()
            raise get_tools_err

        # Create CrewAI tools using the factory
        factory = MCPToolFactory(self._worker)
        created_tools: List[BaseTool] = []
        for mcp_tool in mcp_tools:
            try:
                tool = factory.create_tool(mcp_tool)
                created_tools.append(tool)
                logger.debug(f"Successfully created CrewAI tool: {tool.name}")
            except Exception as tool_create_error:
                # Log error but continue creating other tools
                logger.error(
                    f"Error creating CrewAI tool for MCP tool '{mcp_tool.name}': {tool_create_error}",
                    exc_info=True,
                )

        self.tools = created_tools

        if not self.tools and mcp_tools:
            # If MCP reported tools but we failed to create any CrewAI versions
            logger.error(
                "Failed to create any CrewAI tools from discovered MCP tools."
            )
            # Optionally, could cleanup and raise an error here if tools are mandatory
        elif not mcp_tools:
            logger.warning("MCP server reported no available tools.")

        logger.info(
            f"MCPToolSet initialized with {len(self.tools)} CrewAI tools."
        )
        return self.tools

    async def batch_execute(
        self, operations: List[Dict[str, Any]]
    ) -> List[Any]:
        """Executes multiple MCP tool operations concurrently.

        Submits all operations to the worker thread and waits for their results.

        Args:
            operations: A list of dictionaries, each specifying an operation:
                {'tool': <tool_name>, 'args': <arguments_dict>}

        Returns:
            A list containing the results of each operation in the same order.
            If an operation fails, its corresponding entry in the list will
            contain an error message string.

        Raises:
            RuntimeError: If the worker thread is not running.
        """
        if not operations:
            return []

        if not self._worker.is_alive():
            raise RuntimeError(
                "Cannot batch execute: MCP Worker thread is not running."
            )

        # Map tool names to available tool instances for validation (optional)
        # tool_map = {tool.name: tool for tool in self.tools} # Requires initialized tools

        futures_map: Dict[int, concurrent.futures.Future] = {}
        error_results: Dict[int, str] = {}

        for i, op in enumerate(operations):
            tool_name = op.get("tool")
            args = op.get("args", {})

            if not isinstance(tool_name, str):
                error_results[i] = f"Error: Operation {i} missing 'tool' name."
                logger.error(error_results[i])
                continue
            if not isinstance(args, dict):
                error_results[i] = (
                    f"Error: Operation {i} ('{tool_name}') 'args' must be a dict."
                )
                logger.error(error_results[i])
                continue

            # Optional: Validate tool exists if self.tools is populated
            # if tool_name not in tool_map:
            #     error_results[i] = f"Error: Tool '{tool_name}' not found for operation {i}."
            #     logger.error(error_results[i])
            #     continue

            try:
                # Submit request without pre-validation (worker handles errors)
                future = self._worker.submit_request(tool_name, args)
                futures_map[i] = future
            except Exception as e:
                error_msg = f"Error submitting request for operation {i} ('{tool_name}'): {e}"
                logger.error(error_msg)
                error_results[i] = error_msg

        # Wait for all submitted futures to complete
        results: List[Any] = [None] * len(operations)
        if futures_map:
            # Get timeout from configuration
            batch_timeout = self._config.batch_execution_timeout

            # Wait for all futures that were successfully submitted
            done, not_done = concurrent.futures.wait(
                futures_map.values(), timeout=batch_timeout
            )

            if not_done:
                logger.warning(
                    f"{len(not_done)} batch operations timed out after {batch_timeout}s."
                )
                # Handle timeouts - associate them back to the original index
                timed_out_indices = {
                    idx for idx, f in futures_map.items() if f in not_done
                }
                for idx in timed_out_indices:
                    error_results[idx] = f"Error: Operation {idx} timed out."
                    # Attempt to cancel the future
                    futures_map[idx].cancel()

        # Collect results, preserving order and including errors
        for i in range(len(operations)):
            if i in error_results:
                results[i] = error_results[i]
                continue
            if i in futures_map:
                future = futures_map[i]
                try:
                    # Use a small timeout since the future should already be done
                    raw_result = future.result(timeout=0.1)

                    # Use shared utility for result processing
                    results[i] = process_mcp_result(raw_result)

                except Exception as e:
                    error_msg = f"Error getting result for operation {i}: {e}"
                    logger.error(error_msg)
                    results[i] = f"Error: {str(e)}"
            else:
                # Should have been caught earlier, but handle defensively
                results[i] = (
                    f"Error: Operation {i} was invalid or not processed."
                )

        return results

    def refresh_tools(self) -> List[BaseTool]:
        """Refreshes the list of tools from the MCP server.

        Queries the MCP server for its current list of tools and updates the
        `self.tools` list, adding any newly discovered tools. Existing tool
        instances are not removed or modified.

        Returns:
            The updated list of CrewAI BaseTool objects.
        """
        if not self._worker.is_alive():
            logger.error("Cannot refresh tools: Worker thread is not running.")
            return self.tools

        logger.info("Refreshing MCP tools list from server...")
        try:
            # Request worker to fetch the latest tool list from the server
            mcp_tools = self._worker.get_tools(force_refresh=True)

            # Identify newly discovered tools
            current_tool_names = {tool.name for tool in self.tools}
            new_mcp_tools = [
                mcp_tool
                for mcp_tool in mcp_tools
                if mcp_tool.name not in current_tool_names
            ]

            if not new_mcp_tools:
                logger.info("No new tools found during refresh.")
                return self.tools

            logger.info(
                f"Found {len(new_mcp_tools)} new MCP tools: {[t.name for t in new_mcp_tools]}"
            )

            # Create CrewAI tools for the new MCP tools
            factory = MCPToolFactory(self._worker)
            added_tools_count = 0
            for mcp_tool in new_mcp_tools:
                try:
                    tool = factory.create_tool(mcp_tool)
                    self.tools.append(tool)
                    added_tools_count += 1
                    logger.info(f"Added new CrewAI tool: {tool.name}")
                except Exception as e:
                    logger.error(
                        f"Error creating CrewAI tool for newly discovered MCP tool '{mcp_tool.name}': {e}",
                        exc_info=True,
                    )

            if added_tools_count > 0:
                logger.info(
                    f"Successfully added {added_tools_count} new tools. Total tools: {len(self.tools)}"
                )
            else:
                logger.warning(
                    "Failed to create CrewAI tools for any new MCP definitions found."
                )

            return self.tools

        except Exception as e:
            logger.error(f"Error during tool refresh: {e}", exc_info=True)
            # Return the potentially outdated list on error
            return self.tools

    def cleanup(self):
        """Stops the worker thread and performs cleanup."""
        if self._worker and self._worker.is_alive():
            logger.info("Cleaning up MCPToolSet: Stopping worker thread...")
            self._worker.stop()
            logger.info("MCPToolSet worker stopped.")
        else:
            logger.debug(
                "MCPToolSet cleanup: Worker already stopped or not initialized."
            )
        # Clear the list of tools
        self.tools = []

    # --- Context Manager Implementation ---

    def __enter__(self) -> List[BaseTool]:
        """Enters the synchronous context manager, initializing the toolset.

        Returns:
            The list of initialized CrewAI tools.
        """
        logger.debug("MCPToolSet entering synchronous context...")
        return self.initialize()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the synchronous context manager, cleaning up resources."""
        logger.debug(
            f"MCPToolSet exiting synchronous context (exception: {exc_type})..."
        )
        self.cleanup()

    async def __aenter__(self) -> List[BaseTool]:
        """Enters the asynchronous context manager, initializing the toolset.

        Note: Initialization itself involves starting a thread and potentially
        blocking waits, so it remains effectively synchronous from the caller's
        perspective, even when called via `async with`.

        Returns:
            The list of initialized CrewAI tools.
        """
        logger.debug("MCPToolSet entering asynchronous context...")
        # Initialization logic is handled within the worker thread startup
        return self.initialize()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exits the asynchronous context manager, cleaning up resources.

        Note: Cleanup involves joining a thread, which is a blocking operation.
        """
        logger.debug(
            f"MCPToolSet exiting asynchronous context (exception: {exc_type})..."
        )
        # Cleanup is synchronous due to thread joining
        self.cleanup()

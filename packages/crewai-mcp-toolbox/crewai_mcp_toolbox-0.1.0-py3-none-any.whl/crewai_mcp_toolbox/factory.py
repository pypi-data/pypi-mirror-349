"""Tool factory for creating CrewAI tools from MCP tool definitions.

This module provides the MCPToolFactory class, which converts MCP tool
definitions into CrewAI-compatible BaseTool instances with the necessary
schema generation and execution logic.
"""

import asyncio
import concurrent.futures
import enum
import logging
from typing import Any, Dict, List, Tuple, Type, Union

from crewai.tools import BaseTool
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    ValidationError,
    create_model,
)

from .exceptions import MCPToolError, MCPToolExecutionError
from .utils import process_mcp_result
from .worker import MCPWorkerThread

# Configure logging
logger = logging.getLogger(__name__)


class MCPToolArgsBase(BaseModel):
    """Base model for dynamically created MCP tool schemas.

    Allows extra fields to accommodate flexible or complex MCP schemas.
    """

    model_config = ConfigDict(extra="allow")


def create_schema_from_mcp_tool(mcp_tool) -> Type[BaseModel]:
    """Dynamically creates a Pydantic model from an MCP tool's input schema.

    Handles basic JSON schema types (string, integer, number, boolean, array,
    object) and attempts to map them to Python types. Uses a flexible base
    model if complex schema constructs (allOf, anyOf, oneOf) are detected.
    Special handling for common pagination parameters (limit, offset, etc.)
    to ensure they are treated as strings if needed by the MCP server,
    even if the schema defines them as numeric.

    Args:
        mcp_tool: The MCPTool object containing the inputSchema definition.

    Returns:
        A Pydantic BaseModel class representing the input schema. Falls back
        to a flexible base model if schema creation fails or is too complex.
    """
    schema_name = f"{mcp_tool.name.replace('-', '_').capitalize()}Schema"
    base_schema = MCPToolArgsBase  # Use the flexible base by default

    if not hasattr(mcp_tool, "inputSchema") or not mcp_tool.inputSchema:
        logger.debug(
            f"MCP tool '{mcp_tool.name}' has no inputSchema. Creating empty schema."
        )
        return create_model(schema_name, __base__=base_schema)

    input_schema = mcp_tool.inputSchema
    properties = input_schema.get("properties", {})
    required = set(input_schema.get("required", []))
    fields: Dict[str, Tuple[Any, Field]] = {}

    # Check for complex schema structures that Pydantic's create_model might not handle well
    if any(k in input_schema for k in ("allOf", "oneOf", "anyOf", "not")):
        logger.warning(
            f"Tool '{mcp_tool.name}' uses complex schema constructs "
            f"(allOf/anyOf/oneOf/not). Using a flexible schema ({base_schema.__name__}) "
            "which allows any fields but performs minimal validation."
        )
        # For complex schemas, return the base flexible model directly without defining fields
        return base_schema

    logger.debug(
        f"Creating schema for '{mcp_tool.name}'. Properties: {properties}, Required: {required}"
    )

    type_mapping: Dict[str, Type] = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "array": list,
        "object": dict,
    }

    for prop_name, prop_details in properties.items():
        if not isinstance(prop_details, dict):
            logger.warning(
                f"Skipping invalid property definition for '{prop_name}' in tool '{mcp_tool.name}'"
            )
            continue

        json_type = prop_details.get("type", "string")
        description = prop_details.get("description", "")
        is_required = prop_name in required
        default_value = prop_details.get("default")

        # MCP often expects pagination params as strings, override schema type if numeric
        if json_type in ["integer", "number"] and prop_name in [
            "limit",
            "offset",
            "page",
            "size",
            "count",
        ]:
            logger.debug(
                f"Mapping numeric schema field '{prop_name}' to string type for MCP."
            )
            python_type: Any = str
        else:
            python_type = type_mapping.get(json_type, Any)

        # Handle enums
        enum_values = prop_details.get("enum")
        if enum_values and isinstance(enum_values, list):
            try:
                # Enum names must be valid Python identifiers
                enum_name = f"{schema_name}{prop_name.capitalize().replace('_', '')}Enum"
                # Create enum members, handling potential type inconsistencies
                enum_members: Dict[str, Any] = {}
                if json_type == "string":
                    enum_members = {
                        str(v): str(v) for v in enum_values if v is not None
                    }
                elif json_type in ["integer", "number"]:
                    # Use names like 'VALUE_0', 'VALUE_1' as keys
                    enum_members = {
                        f"VALUE_{i}": v
                        for i, v in enumerate(enum_values)
                        if v is not None
                    }
                elif json_type == "boolean":
                    enum_members = {
                        "TRUE": True,
                        "FALSE": False,
                    }  # Assuming standard bools
                else:  # Fallback for other types: use string representation
                    enum_members = {
                        f"VALUE_{i}": str(v)
                        for i, v in enumerate(enum_values)
                        if v is not None
                    }

                if enum_members:
                    python_type = enum.Enum(enum_name, enum_members)
                    logger.debug(
                        f"Created Enum '{enum_name}' for '{prop_name}'"
                    )
                else:
                    logger.warning(
                        f"Enum values for '{prop_name}' in '{mcp_tool.name}' resulted in empty mapping. Using base type {python_type}."
                    )
            except Exception as e:
                logger.warning(
                    f"Could not create Enum for '{prop_name}' in '{mcp_tool.name}': {e}. Using base type {python_type}."
                )

        # Handle arrays with specified item types
        if python_type is list and "items" in prop_details:
            items_schema = prop_details["items"]
            if isinstance(items_schema, dict):
                item_json_type = items_schema.get("type", "string")
                item_python_type = type_mapping.get(item_json_type, Any)
                python_type = List[item_python_type]
                logger.debug(
                    f"Mapping array field '{prop_name}' to List[{item_python_type.__name__}]"
                )

        # Define the Pydantic field
        field_args = {"description": description}
        if is_required:
            field_info = Field(..., **field_args)
            final_type = python_type
        else:
            # Use Union[python_type, None] which becomes Optional[python_type]
            field_args["default"] = default_value
            field_info = Field(**field_args)
            final_type = Union[python_type, None]

        fields[prop_name] = (final_type, field_info)
        logger.debug(
            f"Added field '{prop_name}' to schema '{mcp_tool.name}': type={final_type}, required={is_required}, default={default_value}"
        )

    # Create the Pydantic model
    try:
        model = create_model(schema_name, **fields, __base__=base_schema)
        logger.debug(
            f"Successfully created Pydantic model '{schema_name}' for tool '{mcp_tool.name}'."
        )
        return model
    except Exception as e:
        logger.error(
            f"Failed to create Pydantic model '{schema_name}' from properties: {e}",
            exc_info=True,
        )
        logger.warning(
            f"Returning fallback schema ({base_schema.__name__}) for tool '{mcp_tool.name}'."
        )
        # Return the flexible base model if creation fails
        return base_schema


class MCPToolFactory:
    """Factory for creating CrewAI BaseTool instances from MCP tool definitions.

    This factory takes an MCP tool definition and wraps it in a CrewAI-compatible
    BaseTool class, dynamically generating the necessary Pydantic input schema
    and providing the execution logic that interacts with the MCPWorkerThread.

    Attributes:
        worker: The MCPWorkerThread instance used for executing tool calls.
    """

    def __init__(self, worker: MCPWorkerThread):
        """Initializes the factory with an MCP worker instance.

        Args:
            worker: The MCPWorkerThread responsible for communicating with the MCP server.

        Raises:
            RuntimeError: If the MCP library is not available.
            TypeError: If the provided worker is not a valid MCPWorkerThread instance.
        """
        if not isinstance(worker, MCPWorkerThread):
            raise TypeError(
                "MCPToolFactory requires a valid MCPWorkerThread instance."
            )
        self.worker = worker

    def create_tool(self, mcp_tool) -> BaseTool:
        """Converts an MCP tool definition into an executable CrewAI BaseTool.

        Args:
            mcp_tool: The MCPTool object retrieved from the MCP server.

        Returns:
            An instance of a dynamically created CrewAI BaseTool subclass
            that represents the MCP tool.

        Raises:
            ValueError: If the provided mcp_tool is invalid (e.g., None or missing name).
        """
        if mcp_tool is None:
            raise ValueError(
                "Cannot create tool from None MCP tool definition."
            )
        if not hasattr(mcp_tool, "name") or not mcp_tool.name:
            raise ValueError(
                "MCP tool definition is missing the 'name' attribute."
            )

        tool_name = mcp_tool.name
        tool_description = (
            mcp_tool.description or f"Interface to the MCP tool '{tool_name}'."
        )

        # Dynamically create the Pydantic schema for argument validation
        try:
            dynamic_schema = create_schema_from_mcp_tool(mcp_tool)
        except Exception as schema_exc:
            logger.error(
                f"Failed to create dynamic schema for tool '{tool_name}'. "
                f"Using a fallback schema. Error: {schema_exc}",
                exc_info=True,
            )
            # Fallback to a generic schema allowing any arguments if creation fails
            dynamic_schema = create_model(
                f"{tool_name.replace('-', '_').capitalize()}FallbackSchema",
                __base__=MCPToolArgsBase,  # Use the flexible base
            )

        # Define the CrewAI Tool class dynamically
        class MCPDynamicTool(BaseTool):
            """A CrewAI tool dynamically generated from an MCP tool definition."""

            name: str = tool_name
            description: str = tool_description
            args_schema: Type[BaseModel] = dynamic_schema
            # Store worker reference privately
            _private_worker: MCPWorkerThread = PrivateAttr()

            async def _arun(self, **kwargs: Any) -> Any:
                """Asynchronous execution (delegates to synchronous _run).

                Note: CrewAI typically uses the synchronous _run method. Direct
                async usage might bypass the intended worker thread queuing.

                Args:
                    **kwargs: Arguments passed to the tool.

                Returns:
                    The result of the tool execution.
                """
                logger.warning(
                    f"MCPDynamicTool '{self.name}' _arun called directly. Delegating to _run."
                )
                # Delegate to _run which handles worker interaction
                # A fully async implementation would require direct interaction
                # with the worker's async mechanisms.
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self._run, **kwargs)

            def _run(self, **kwargs: Any) -> Any:
                """Synchronous execution wrapper for the MCP tool call.

                Validates input arguments against the generated schema, submits
                the request to the MCPWorkerThread, waits for the result, and
                processes the response.

                Args:
                    **kwargs: Arguments passed to the tool.

                Returns:
                    The processed result from the MCP tool call, or an error string
                    if execution fails or times out.
                """
                logger.debug(
                    f"MCPDynamicTool '{self.name}' _run called with kwargs: {kwargs}"
                )

                if (
                    not hasattr(self, "_private_worker")
                    or not self._private_worker
                ):
                    error_msg = f"Tool '{self.name}' is missing the MCP worker instance."
                    logger.critical(error_msg)  # Critical config error
                    return f"Configuration Error: {error_msg}"

                if not self._private_worker.is_alive():
                    error_msg = f"MCP Worker thread for tool '{self.name}' is not running."
                    logger.error(error_msg)
                    # Attempt to restart or notify? For now, return error.
                    return f"Error: {error_msg}"

                try:
                    # --- Input Validation ---
                    try:
                        # Validate provided kwargs against the dynamic schema
                        validated_args = self.args_schema.model_validate(
                            kwargs
                        )
                        # Use model_dump to get dict, respecting aliases etc.
                        args_to_send = validated_args.model_dump()
                        logger.debug(
                            f"Validated args for '{self.name}': {args_to_send}"
                        )
                    except ValidationError as e:
                        error_msg = (
                            f"Invalid input for tool '{self.name}': {e}"
                        )
                        logger.error(f"{error_msg} (Input: {kwargs})")
                        # Provide clear error message to the agent/user
                        return f"Error: {error_msg}"

                    # Submit request to the worker and get a Future
                    future = self._private_worker.submit_request(
                        self.name, args_to_send
                    )

                    # Get timeout from worker's config if available
                    tool_timeout = getattr(
                        self._private_worker._config,
                        "tool_execution_timeout",
                        90.0,
                    )  # seconds

                    logger.debug(
                        f"Waiting up to {tool_timeout}s for result from tool '{self.name}'..."
                    )
                    result = future.result(timeout=tool_timeout)

                    # --- Process Result using shared utility ---
                    logger.debug(
                        f"Tool '{self.name}' received raw result from worker: {type(result)}"
                    )

                    processed_result = process_mcp_result(result)

                    logger.debug(
                        f"Tool '{self.name}' processed result: {type(processed_result)}"
                    )
                    return (
                        processed_result
                        if processed_result is not None
                        else f"MCP tool '{self.name}' returned empty or unprocessable content."
                    )
                    # --- End Result Processing ---

                except concurrent.futures.TimeoutError:
                    # Catches future.result(timeout=...) timeout
                    error_msg = (
                        f"Tool execution timed out for '{self.name}' after "
                        f"{tool_timeout} seconds (waiting for worker response)."
                    )
                    logger.error(error_msg)
                    return f"Error: {error_msg}"
                except Exception as e:
                    # Catches exceptions from submit_request, future.result(),
                    # or processing logic.
                    error_msg = f"Error executing tool '{self.name}' via worker: {str(e)}"
                    # Log full trace for unexpected errors, less detail for known types
                    log_as_exception = not isinstance(
                        e, (MCPToolError, ValueError, TypeError, TimeoutError)
                    )
                    logger.error(error_msg, exc_info=log_as_exception)
                    return f"Error: {error_msg}"

        # Instantiate the dynamic tool and inject the worker reference
        tool_instance = MCPDynamicTool()
        tool_instance._private_worker = self.worker
        logger.debug(f"Created CrewAI tool instance for '{tool_name}'")
        return tool_instance

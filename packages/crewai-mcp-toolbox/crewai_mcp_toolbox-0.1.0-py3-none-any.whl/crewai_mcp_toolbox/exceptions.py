"""Exception classes for MCP integration.

This module defines the exceptions that may be raised during MCP tool discovery,
validation, and execution.
"""


class MCPToolError(Exception):
    """Base exception for MCP tool related errors."""


class MCPToolNotFoundError(MCPToolError):
    """Exception raised when an MCP tool cannot be found."""


class MCPToolInputError(MCPToolError):
    """Exception raised for errors in MCP tool input validation."""


class MCPToolExecutionError(MCPToolError):
    """Exception raised when an MCP tool fails during execution."""


class MCPConnectionError(MCPToolError):
    """Exception raised when there is an error in MCP connection or communication."""

    pass  # No additional logic needed for now


class MCPProcessError(MCPToolError):
    """Exception raised when the MCP server process fails or cannot be managed."""

    pass  # No additional logic needed for now

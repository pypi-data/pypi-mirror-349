"""Utility functions for MCP integration.

This module provides shared utility functions used across various components
of the MCP integration package.
"""

import json
import logging
from typing import Any, Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)


def process_mcp_result(raw_result: Any) -> Any:
    """Process raw MCP tool results into a more usable format.

    Extracts content from common MCP result patterns, simplifies list structures,
    and attempts to parse JSON strings when appropriate.

    Args:
        raw_result: The raw result returned from an MCP tool call

    Returns:
        Processed result in the most appropriate Python type
    """
    # Extract content from common MCP result patterns
    processed_result: Any = None
    if hasattr(raw_result, "content"):
        processed_result = raw_result.content
    elif hasattr(raw_result, "result"):
        processed_result = raw_result.result
    elif hasattr(raw_result, "data"):
        processed_result = raw_result.data
    else:
        # Fallback if no known attribute found
        processed_result = raw_result

    # Simplify common result types (e.g., single text item in a list)
    if isinstance(processed_result, list) and len(processed_result) == 1:
        item = processed_result[0]
        # Prefer text attribute if available (common in MCP text responses)
        processed_result = getattr(item, "text", item)

    # Attempt to parse JSON string content
    if isinstance(processed_result, str):
        try:
            # Basic check if it looks like JSON before attempting parse
            stripped_content = processed_result.strip()
            if (
                stripped_content.startswith("{")
                and stripped_content.endswith("}")
            ) or (
                stripped_content.startswith("[")
                and stripped_content.endswith("]")
            ):
                processed_result = json.loads(processed_result)
                logger.debug("Successfully parsed JSON string result")
        except json.JSONDecodeError:
            # Keep as string if parsing fails
            pass

    logger.debug(f"Processed MCP result: {type(processed_result).__name__}")
    return processed_result


class MCPConfiguration:
    """Configuration container for MCP integration components.

    Provides default values and validation for configuration parameters
    used across the MCP integration package.
    """

    DEFAULT_CONFIG = {
        "worker_startup_timeout": 60.0,  # Seconds to wait for worker thread startup
        "tool_execution_timeout": 90.0,  # Seconds to wait for tool execution
        "batch_execution_timeout": 180.0,  # Seconds to wait for batch operations
        "per_call_timeout": 60.0,  # Seconds to wait for individual MCP calls
        "health_check_interval": 10.0,  # Seconds between worker health checks
    }

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize configuration with defaults and optional overrides.

        Args:
            config: Optional dictionary of configuration parameters to override defaults
        """
        self._config = self.DEFAULT_CONFIG.copy()

        if config:
            # Update with user-provided values
            for key, value in config.items():
                if key in self._config:
                    # Basic validation for timeout values
                    if key.endswith("_timeout") and (
                        not isinstance(value, (int, float)) or value <= 0
                    ):
                        logger.warning(
                            f"Invalid timeout value for '{key}': {value}. Using default: {self._config[key]}"
                        )
                        continue
                    self._config[key] = value
                else:
                    logger.warning(f"Unknown configuration parameter: '{key}'")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get a configuration value.

        Args:
            key: The configuration parameter name
            default: Optional default value if the key is not found

        Returns:
            The configuration value or the default
        """
        return self._config.get(key, default)

    @property
    def worker_startup_timeout(self) -> float:
        """Seconds to wait for worker thread startup."""
        return self._config["worker_startup_timeout"]

    @property
    def tool_execution_timeout(self) -> float:
        """Seconds to wait for tool execution."""
        return self._config["tool_execution_timeout"]

    @property
    def batch_execution_timeout(self) -> float:
        """Seconds to wait for batch operations."""
        return self._config["batch_execution_timeout"]

    @property
    def per_call_timeout(self) -> float:
        """Seconds to wait for individual MCP calls."""
        return self._config["per_call_timeout"]

    @property
    def health_check_interval(self) -> float:
        """Seconds between worker health checks."""
        return self._config["health_check_interval"]

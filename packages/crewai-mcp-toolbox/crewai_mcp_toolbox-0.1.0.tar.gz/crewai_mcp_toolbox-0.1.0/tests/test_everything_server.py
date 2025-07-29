# src/crewai_mcp_toolbox/tests/test_everything_server.py
import asyncio  # Keep if needed
import json

import pytest

from crewai_mcp_toolbox import MCPToolSet

# REMOVE the anext helper function


# This test uses the 'everything_mcp_server' fixture defined in conftest.py


@pytest.mark.asyncio
async def test_everything_server_initialization(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Verify the 'everything' server starts and tools are loaded."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools = everything_mcp_server.tools
    assert tools, "No tools were loaded from the 'everything' MCP server."
    print(
        f"\nAvailable 'everything' MCP tools: {[tool.name for tool in tools]}"
    )
    expected_tools = {
        "echo",
        "add",
        "printEnv",
        "longRunningOperation",
        "annotatedMessage",
        "getResourceReference",
    }
    loaded_tool_names = {tool.name for tool in tools}
    assert expected_tools.issubset(
        loaded_tool_names
    ), f"Missing expected tools: {expected_tools - loaded_tool_names}"


@pytest.mark.asyncio
async def test_everything_echo(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'echo' tool."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "echo" in tools_dict, "'echo' tool not found."
    echo_tool = tools_dict["echo"]

    message = "Hello from pytest for everything server!"
    result = echo_tool._run(message=message)
    print(f"Echo result: {result}")

    expected_content = f"Echo: {message}"
    assert (
        result == expected_content
    ), f"Expected '{expected_content}', got '{result}'"


@pytest.mark.asyncio
async def test_everything_add(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'add' tool."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "add" in tools_dict, "'add' tool not found."
    add_tool = tools_dict["add"]

    a, b = 111, 222
    result = add_tool._run(a=a, b=b)
    print(f"Add result: {result} ({type(result)})")
    expected_sum_str = str(a + b)

    assert isinstance(
        result, str
    ), f"Expected result to be string, got {type(result)}"
    assert (
        expected_sum_str in result
    ), f"Expected sum '{expected_sum_str}' to be in result string '{result}'"


@pytest.mark.asyncio
async def test_everything_print_env(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'printEnv' tool."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "printEnv" in tools_dict, "'printEnv' tool not found."
    print_env_tool = tools_dict["printEnv"]

    result = print_env_tool._run()
    print(f"PrintEnv result (sample): {str(result)[:150]}...")

    assert isinstance(
        result, dict
    ), f"Expected printEnv result to be processed into a dict, got {type(result)}"
    assert any(
        key.upper() == "PATH" for key in result.keys()
    ), "Expected 'PATH' (case-insensitive) variable in environment variables."


@pytest.mark.asyncio
async def test_everything_long_running(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'longRunningOperation' tool."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "longRunningOperation" in tools_dict
    tool = tools_dict["longRunningOperation"]
    result = tool._run(duration=2, steps=1)
    print(f"Long running result: {result}")
    assert (
        isinstance(result, str) and "completed" in result.lower()
    ), f"Expected completion message, got: {result}"


@pytest.mark.asyncio
async def test_everything_annotated_message(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'annotatedMessage' tool for different types."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "annotatedMessage" in tools_dict
    tool = tools_dict["annotatedMessage"]

    for msg_type in ["error", "success", "debug"]:
        print(f"\nTesting annotatedMessage type: {msg_type}")
        result = tool._run(messageType=msg_type, includeImage=False)
        print(f"Result: {result} ({type(result)})")

        assert isinstance(
            result, str
        ), f"Expected string result for annotatedMessage type '{msg_type}', got {type(result)}"
        assert (
            len(result) > 0
        ), f"Expected non-empty string for type '{msg_type}'"
        if msg_type == "error":
            assert "error" in result.lower()
        elif msg_type == "success":
            assert "success" in result.lower()


@pytest.mark.asyncio
async def test_everything_get_resource_reference(
    everything_mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'getResourceReference' tool."""
    assert isinstance(everything_mcp_server, MCPToolSet)  # Optional check

    tools_dict = {tool.name: tool for tool in everything_mcp_server.tools}
    assert "getResourceReference" in tools_dict
    tool = tools_dict["getResourceReference"]

    resource_id = 99
    result = tool._run(resourceId=resource_id)
    print(f"Get resource result: {result} ({type(result)})")

    assert isinstance(
        result, list
    ), f"Expected list result for getResourceReference, got {type(result)}"
    assert len(result) > 0, "Expected non-empty list for resource reference"

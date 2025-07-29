# src/crewai_mcp_toolbox/tests/test_docker_server.py
import asyncio  # Keep asyncio if needed for other async operations, but not for fixtures
import json
from typing import List

import pytest

from crewai_mcp_toolbox import MCPToolSet

# BaseTool not needed here

# Define the server configuration once
DOCKER_MCP_CONFIG = {"command": "uvx", "args": ["docker-mcp"]}

# REMOVE the anext helper function


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mcp_server", [DOCKER_MCP_CONFIG], indirect=True, scope="function"
)
async def test_docker_server_initialization(
    mcp_server: MCPToolSet,
):  # Use fixture directly
    """Verify the Docker MCP server starts and tools are loaded."""
    # Fixture is already the MCPToolSet instance yielded
    assert isinstance(
        mcp_server, MCPToolSet
    ), "Fixture did not yield MCPToolSet instance"  # Optional check

    tools = mcp_server.tools
    assert tools, "No tools were loaded from the Docker MCP server."
    print(f"\nAvailable Docker MCP tools: {[tool.name for tool in tools]}")
    assert any(
        tool.name == "list-containers" for tool in tools
    ), "'list-containers' tool not found."


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mcp_server", [DOCKER_MCP_CONFIG], indirect=True, scope="function"
)
async def test_docker_list_containers(
    mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test the 'list-containers' tool directly."""
    assert isinstance(mcp_server, MCPToolSet)  # Optional check

    tools = mcp_server.tools
    list_tool = next((t for t in tools if t.name == "list-containers"), None)
    assert list_tool is not None, "'list-containers' tool not found."

    print(f"\nTesting '{list_tool.name}' tool via its _run() method...")
    try:
        result = list_tool._run()

        print(f"Result from {list_tool.name}._run():")
        if isinstance(result, (dict, list)):
            print(json.dumps(result, indent=2))
            assert isinstance(
                result, list
            ), f"Expected result to be a list, got {type(result)}"
        else:
            print(result)
            assert not (
                isinstance(result, str) and result.startswith("Error:")
            ), f"Tool reported an error message: {result}"

    except Exception as tool_run_exc:
        pytest.fail(f"Error calling {list_tool.name}._run(): {tool_run_exc}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mcp_server", [DOCKER_MCP_CONFIG], indirect=True, scope="function"
)
async def test_docker_inspect_container_nonexistent(
    mcp_server: MCPToolSet,
):  # Use fixture directly
    """Test inspecting a likely non-existent container."""
    assert isinstance(mcp_server, MCPToolSet)  # Optional check

    tools = mcp_server.tools
    inspect_tool = next(
        (t for t in tools if t.name == "inspect-container"), None
    )
    if inspect_tool is None:
        pytest.skip("'inspect-container' tool not found, skipping test.")
        return

    non_existent_id = "pytest_non_existent_container_12345"
    print(
        f"\nTesting '{inspect_tool.name}' with non-existent ID: {non_existent_id}..."
    )
    try:
        result = inspect_tool._run(container_id=non_existent_id)
        print(f"Result from {inspect_tool.name}._run(): {result}")
        assert (
            isinstance(result, str) and "error" in result.lower()
        ), f"Expected an error message for non-existent container, got: {result}"

    except Exception as inspect_exc:
        pytest.fail(f"Error calling {inspect_tool.name}._run(): {inspect_exc}")

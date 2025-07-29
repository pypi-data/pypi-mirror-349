# crewai-mcp-toolbox: Seamless MCP Integration for CrewAI Agents

[![PyPI version](https://badge.fury.io/py/crewai-mcp-toolbox.svg)](https://badge.fury.io/py/crewai-mcp-toolbox)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Unlock the power of the Model Context Protocol (MCP) directly within your CrewAI agents.**

`crewai-mcp-toolbox` provides a robust and developer-friendly bridge between the CrewAI framework and any compliant MCP server communicating via **stdio**. It automatically discovers tools exposed by an MCP server, converts them into type-safe CrewAI `BaseTool` instances, and reliably manages the underlying server process lifecycle for you.

## The Problem: Integrating MCP Servers Can Be Tricky

The Model Context Protocol standardizes how AI models interact with external tools and data sources. While powerful, integrating an MCP server into an agent framework like CrewAI often involves repetitive and error-prone tasks:

1. **Manual Process Management:** Starting and stopping the MCP server process reliably alongside your agent application.
2. **Boilerplate Communication:** Writing code to handle the `stdio` communication, request/response cycles, and error handling defined by the MCP specification.
3. **Tool Discovery & Wrapping:** Manually fetching the list of tools from the server and writing wrapper classes for each one to make them compatible with CrewAI's `BaseTool`.
4. **Argument Handling:** Ensuring arguments passed from the agent are correctly formatted and validated against the MCP tool's schema.
5. **Reliability:** Monitoring the MCP server process and handling potential crashes or hangs gracefully.

## Why `crewai-mcp-toolbox`? Robustness and Developer Experience

`crewai-mcp-toolbox` tackles these challenges head-on, offering more than just a simple wrapper:

* **Reliable Lifecycle via Dedicated Worker:** At its core, `crewai-mcp-toolbox` uses a dedicated background worker thread (`MCPWorkerThread`) to isolate and manage the MCP server's lifecycle and communication. This ensures the server starts correctly, runs reliably in the background, and is terminated cleanly when your application exits or the context manager scope is left.
* **Proven STDIO Process Control:** For `stdio`-based servers, the worker thread currently utilizes Python's robust `asyncio.create_subprocess_exec` to directly manage the server process. While leveraging native library clients like `mcp.client.stdio.stdio_client` was explored, this direct management approach proved more reliable across different server types during testing (like `uvx`-based servers), ensuring compatibility and preventing hangs observed with the library client in specific scenarios.
* **Dynamic & Typed Tools:** Automatically generates Pydantic models from the MCP server's `inputSchema` for each tool. This provides type hinting, validation, and seamless integration with CrewAI's argument handling, significantly reducing runtime errors.
* **Effortless Integration:** The `MCPToolSet` acts as a simple context manager (`async with`), abstracting away the complexities of process management, threading, and protocol handling. Get a list of ready-to-use CrewAI tools with just a few lines of code.
* **Production-Ready Design:** Built with explicit error handling, configurable timeouts, concurrent request management via futures, and basic health checking in mind.

## Key Features

* **Dynamic Tool Creation:** Automatically discovers tools from any MCP server via `stdio`.
* **Managed Server Lifecycle:** Starts and reliably stops the configured MCP server process using `MCPToolSet` as a context manager, managed by the background worker.
* **Direct STDIO Process Management:** Reliably starts/stops `stdio` servers using `asyncio` primitives within the worker thread for proven compatibility.
* **Protocol Layer via `mcp` Library:** Uses the core `mcp.ClientSession` for handling MCP protocol message details once the stdio streams are established.
* **Robust Background Worker:** Manages communication with the MCP server in a separate thread, handling requests, responses, and errors asynchronously.
* **Health Monitoring:** Includes basic health checking of the underlying MCP server connection status.
* **Typed Arguments:** Generates Pydantic models for tool arguments based on the server's schema, providing validation and type safety.
* **Simple `async with` Interface:** Easily integrate MCP tools into your async CrewAI applications.
* **Flexible Configuration:** Supports launching MCP servers via `npx` for common types (like `server-filesystem`) or by specifying a custom command and arguments.
* **Configurable Timeouts:** Control timeouts for server startup, tool execution, and individual MCP calls.
* **STDIO Focus:** Current implementation is focused on and tested with `stdio`-based MCP servers. (*SSE support is planned for future versions.*)

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate # or .\.venv\Scripts\activate on Windows

# Install the toolbox
pip install crewai-mcp-toolbox

# Ensure you have necessary MCP server dependencies installed
# e.g., for server-filesystem or other Node.js servers:
# npm install -g npx
# e.g., for uvx based servers:
# pip install uvx build # or equivalent uv/pip install build uvx
```

## Quick Start

Integrate MCP tools into your CrewAI agent with minimal setup:

```python
import asyncio
from crewai import Agent, Task, Crew
from crewai_mcp_toolbox import MCPToolSet

async def main():
    # Example 1: Using a filesystem server (requires Node.js/npx)
    # This will start 'npx @modelcontextprotocol/server-filesystem ./my_mcp_data'
    # The directory will be created if it doesn't exist.
    print("Starting Filesystem MCP Server...")
    async with MCPToolSet(directory_path="./my_mcp_data") as filesystem_tools:
        print(f"Filesystem Tools Found: {[tool.name for tool in filesystem_tools]}")
        if not filesystem_tools:
            print("Warning: No filesystem tools discovered. Ensure server started correctly.")
            return # Exit if no tools found

        # Example Agent using these tools (add your LLM details)
        # fs_agent = Agent(...)
        # task = Task(...)
        # crew = Crew(...)
        # result = await crew.kickoff_async()
        # print("Filesystem Crew Result:", result)

    print("-" * 20)
    print("Filesystem MCP Server Stopped.")

    # Example 2: Using a custom command (e.g., a Python-based MCP server)
    # Assumes 'uvx my-custom-mcp-server' starts an MCP server
    print("Starting Custom MCP Server...")
    # Ensure 'my-custom-mcp-server' is runnable via 'uvx' in your environment
    try:
        async with MCPToolSet(command="uvx", args=["my-custom-mcp-server"]) as custom_tools:
            print(f"Custom Tools Found: {[tool.name for tool in custom_tools]}")
            if not custom_tools:
                 print("Warning: No custom tools discovered. Ensure server command is correct and functional.")
                 return # Exit if no tools found

            # Example Agent using these tools (add your LLM details)
            # custom_agent = Agent(...)
            # task = Task(...)
            # crew = Crew(...)
            # result = await crew.kickoff_async()
            # print("Custom Crew Result:", result)

    except FileNotFoundError:
         print("Error: 'uvx' command not found. Make sure uvx is installed and in your PATH.")
    except Exception as e:
         print(f"Error running custom server: {e}") # Catch other potential errors

    print("-" * 20)
    print("Custom MCP Server Stopped (or failed to start).")


if __name__ == "__main__":
    # Basic check if main can run
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
```

## How It Works

- **MCPToolSet**: The main entry point. Acts as an async context manager. Takes configuration (directory_path or command/args) for the STDIO MCP server.
- **MCPWorkerThread**: A background thread started by MCPToolSet.
  - For STDIO, it uses asyncio.create_subprocess_exec to launch the MCP server subprocess directly.
  - It captures the stdin, stdout, and stderr streams of the subprocess.
  - It establishes an mcp.ClientSession using the captured stdout (as reader) and stdin (as writer).
  - It handles the MCP protocol communication (initialize, list_tools, call_tool) via the ClientSession.
  - It monitors connection health via list_tools.
  - It ensures the subprocess is terminated when the context manager exits or cleanup() is called.
- **MCPToolFactory**: Used internally by MCPToolSet. When the worker connects and lists tools, the factory dynamically creates CrewAI BaseTool subclasses for each MCP tool, generating a Pydantic args_schema from the server's inputSchema. Each created tool holds a reference to the worker for execution.
- **Execution**: When an agent calls a tool's _run method, the call is validated against the Pydantic schema, submitted to the MCPWorkerThread, executed over the MCP connection via ClientSession.call_tool, and the processed result is returned.

## Configuration

You can customize timeouts by passing a config dictionary during MCPToolSet initialization:

```python
config = {
    "worker_startup_timeout": 60.0,    # Default: 60s
    "tool_execution_timeout": 120.0,   # Default: 90s (for the CrewAI tool call wrapper)
    "batch_execution_timeout": 180.0,  # Default: 180s (for batch_execute method)
    "per_call_timeout": 45.0,          # Default: 60s (for the underlying MCP ClientSession.call_tool)
    "health_check_interval": 15.0      # Default: 10s
}

`health_check_interval` controls how frequently the worker verifies the MCP
server connection. Lower values detect failures sooner but may increase
overhead.

# Make sure the directory exists or the command is valid
try:
    async with MCPToolSet(directory_path="./data", config=config) as tools:
        print("Tools with custom config:", [t.name for t in tools])
        # ... use tools ...
except Exception as e:
    print(f"Failed to initialize MCPToolSet with custom config: {e}")
```

## Testing

Tests are located in the tests directory and use pytest. Fixtures in tests/conftest.py handle setting up different MCP server types (Docker, Chroma, Everything Server) via STDIO.

To run tests:

```bash
# Install testing requirements (ensure you have pytest, pytest-asyncio etc.)
# Example: pip install -e .[dev] or pip install -r requirements-dev.txt

# Run tests from the project root directory
pytest tests/
```

Note: Some tests may require external dependencies like Docker, Node.js (npx), or specific Python packages (uvx, chroma-mcp). The 'everything' server test fixture clones and builds an external repository.

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, make your changes, add tests, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

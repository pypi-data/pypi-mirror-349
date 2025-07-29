# src/crewai_mcp_toolbox/tests/conftest.py
import asyncio
import json
import os
import shutil
import subprocess
import tempfile
import uuid
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, Generator, Tuple

import pytest
import pytest_asyncio  # Use pytest_asyncio decorator

# Import BaseTool from its correct location
from crewai.tools import BaseTool

# Import your own package components
from crewai_mcp_toolbox import MCPToolSet


# Add print helper for tests when using -s
def test_print(msg: str):
    """Helper for visible output during pytest -s"""
    print(f"[Fixture] {msg}", flush=True)


# --- Configuration ---
# Example: os.environ["OPENAI_API_KEY"] = "your_key_here"
LLM_MODEL = "openai/gpt-4o-mini" if os.environ.get("OPENAI_API_KEY") else None

# --- Fixtures ---


@pytest.fixture(scope="function")
def temp_data_dir(tmp_path: Path) -> Path:
    """Creates a temporary data directory for tests needing filesystem access."""
    data_dir = tmp_path / "mcp_test_data"
    data_dir.mkdir()
    test_print(f"Created temp data dir: {data_dir}")
    yield data_dir
    # Cleanup is handled automatically by pytest's tmp_path fixture
    test_print(f"Cleaning up temp data dir: {data_dir}")


# Removing custom event_loop fixture as it causes warnings and pytest-asyncio handles it.
# Rely on pytest-asyncio's default loop management or configure scope in pyproject.toml.
# @pytest.fixture(scope="session")
# def event_loop(): ...


# Generic MCP Server Fixture (using async generator)
# Use pytest_asyncio.fixture decorator
@pytest_asyncio.fixture(scope="function")
async def mcp_server(request) -> AsyncGenerator[MCPToolSet, None]:
    """
    Starts an MCP server defined by test parameters and yields the MCPToolSet.
    Handles automatic cleanup via MCPToolSet's context management.
    """
    config = getattr(request, "param", {})
    command = config.get("command")
    args = config.get("args", [])
    directory_path = config.get("directory_path")
    env = config.get("env")
    mcp_config = config.get("mcp_config")

    if not command and not directory_path:
        pytest.fail("Fixture parameter requires 'command' or 'directory_path'")

    fixture_id = f"{command or 'dir'} {args or directory_path}"  # For logging
    toolset = MCPToolSet(
        command=command,
        args=args,
        directory_path=directory_path,
        env=env,
        config=mcp_config,
    )

    try:
        test_print(f"({fixture_id}) Entering fixture setup...")
        # MCPToolSet's __aenter__ handles initialization
        async with toolset as tools:
            test_print(
                f"({fixture_id}) MCPToolSet context entered, yielded {len(tools)} tools."
            )
            # Worker startup success is checked within toolset.initialize() called by __aenter__
            # If __aenter__ fails, async with will raise exception.
            yield toolset  # Yield the initialized toolset instance
        test_print(
            f"({fixture_id}) MCPToolSet context normally exited (__aexit__ completed)."
        )

    except Exception as e:
        # This catches errors during __aenter__ or if the test using the fixture fails badly
        test_print(
            f"({fixture_id}) Exception during fixture setup/yield/context exit: {e}"
        )
        # __aexit__ (cleanup) should have been called by async with, but log anyway
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                f"({fixture_id}) Worker might still be alive after exception, attempting cleanup again."
            )
            toolset.cleanup()  # Attempt cleanup again just in case
        # Re-raise or fail the test
        pytest.fail(f"({fixture_id}) MCP server fixture failed: {e}")
    finally:
        # This block runs after the fixture scope ends (after test completes and context exits)
        test_print(f"({fixture_id}) Fixture teardown (finally block) reached.")
        # Double-check worker status after everything
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                f"({fixture_id}) WARNING: Worker thread still alive in fixture finally block!"
            )
        else:
            test_print(
                f"({fixture_id}) Worker confirmed stopped in fixture finally block."
            )


# --- Chroma-specific Fixture ---
# Use pytest_asyncio.fixture decorator
@pytest_asyncio.fixture(scope="function")
async def chroma_mcp_setup(
    temp_data_dir: Path,
) -> AsyncGenerator[Tuple[Dict[str, BaseTool], str], None]:
    """
    Sets up a Chroma MCP server, creates a collection, adds sample data,
    and yields the tools dictionary and collection name.
    """
    collection_name = f"pytest_collection_{uuid.uuid4().hex[:8]}"
    command = "uvx"
    args = [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        str(temp_data_dir),
    ]

    # Define SAMPLE_DATA here
    SAMPLE_TEXTS = [
        "Chroma DB info...",
        "MCP info...",
        "Server info...",
        "Search info...",
        "Embedding info...",
    ]
    SAMPLE_METADATA = [
        {"cat": "intro"},
        {"cat": "protocol"},
        {"cat": "feat"},
        {"cat": "search"},
        {"cat": "embed"},
    ]

    toolset = MCPToolSet(command=command, args=args)
    tools_dict: Dict[str, BaseTool] = {}

    try:
        test_print(
            f"[Chroma] Initializing Chroma MCP Server in {temp_data_dir}..."
        )
        async with toolset as tools:
            test_print("[Chroma] Server context entered.")
            # initialize checks worker status
            if not toolset._worker or not toolset._worker._startup_success:
                pytest.fail(
                    "[Chroma] MCP Worker failed during startup in fixture."
                )

            tools_dict = {tool.name: tool for tool in tools}
            if not tools_dict.get(
                "chroma_create_collection"
            ) or not tools_dict.get("chroma_add_documents"):
                pytest.fail(
                    f"[Chroma] Core tools missing. Found: {list(tools_dict.keys())}"
                )

            test_print(f"[Chroma] Loaded tools: {list(tools_dict.keys())}")

            # --- Initial Data Setup ---
            test_print(f"[Chroma] Setting up collection: {collection_name}")
            create_tool = tools_dict["chroma_create_collection"]
            create_result = create_tool._run(
                collection_name=collection_name
            )  # Sync call
            test_print(f"[Chroma] Create collection result: {create_result}")
            if isinstance(create_result, str) and create_result.startswith(
                "Error:"
            ):
                pytest.fail(
                    f"Failed to create collection in fixture: {create_result}"
                )

            add_tool = tools_dict["chroma_add_documents"]
            doc_ids = [f"doc_{i}" for i in range(len(SAMPLE_TEXTS))]
            metadatas_json_str = json.dumps(SAMPLE_METADATA)
            ids_json_str = json.dumps(doc_ids)
            documents_list = SAMPLE_TEXTS
            add_result = add_tool._run(
                collection_name=collection_name,
                documents=documents_list,
                metadatas=metadatas_json_str,
                ids=ids_json_str,
            )  # Sync call
            test_print(f"[Chroma] Add documents result: {add_result}")
            if isinstance(add_result, str) and add_result.startswith("Error:"):
                pytest.fail(
                    f"Failed to add documents in fixture: {add_result}"
                )

            test_print("[Chroma] Setup complete. Yielding tools and name...")
            yield tools_dict, collection_name
            test_print("[Chroma] Resumed after yield.")

        test_print("[Chroma] Context exited.")

    except Exception as e:
        test_print(f"[Chroma] Error during setup/yield/context exit: {e}")
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                f"[Chroma] Worker might still be alive after exception, attempting cleanup again."
            )
            toolset.cleanup()
        pytest.fail(f"Chroma setup fixture failed: {e}")
    finally:
        test_print("[Chroma] Fixture teardown (finally block) reached.")
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                "[Chroma] WARNING: Worker thread still alive in fixture finally block!"
            )
        else:
            test_print(
                "[Chroma] Worker confirmed stopped in fixture finally block."
            )


# --- Everything Server Fixture ---
# This is synchronous fixture for the build step
@pytest.fixture(scope="session")
def built_everything_server_path() -> Generator[str, None, None]:
    """Clones, builds the 'everything' server and yields the path to the built index.js."""
    with tempfile.TemporaryDirectory() as temp_dir:
        server_path = None
        original_cwd = os.getcwd()
        test_print(
            f"[BuildEverything] Setting up 'everything' server build in {temp_dir}"
        )
        try:
            test_print("[BuildEverything] Cloning servers repo...")
            subprocess.run(
                [
                    "git",
                    "clone",
                    "--depth",
                    "1",
                    "https://github.com/modelcontextprotocol/servers.git",
                    temp_dir,
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )

            everything_dir = Path(temp_dir) / "src" / "everything"
            if not everything_dir.is_dir():
                pytest.fail(
                    f"Cloned repo missing expected directory: {everything_dir}"
                )

            os.chdir(everything_dir)
            test_print(
                "[BuildEverything] Installing dependencies (npm install)..."
            )
            subprocess.run(
                ["npm", "install", "--quiet"],
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
            )
            test_print("[BuildEverything] Building server (npm run build)...")
            subprocess.run(
                ["npm", "run", "build"],
                check=True,
                capture_output=True,
                text=True,
                timeout=60,
            )

            server_path = str(everything_dir / "dist" / "index.js")
            if not os.path.exists(server_path):
                pytest.fail(f"Built server not found at {server_path}")

            test_print(
                f"[BuildEverything] Build complete. Server path: {server_path}"
            )
            yield server_path

        except subprocess.CalledProcessError as e:
            print(
                f"[BuildEverything] Error during build process command: {e.cmd}"
            )
            print(f"[BuildEverything] Return code: {e.returncode}")
            print(f"[BuildEverything] Stdout:\n{e.stdout}")
            print(f"[BuildEverything] Stderr:\n{e.stderr}")
            pytest.fail(f"Failed to build 'everything' server: {e}")
        except subprocess.TimeoutExpired as e:
            print(
                f"[BuildEverything] Timeout during build process command: {e.cmd}"
            )
            pytest.fail(f"Timeout building 'everything' server: {e}")
        except Exception as e:
            pytest.fail(f"Unexpected error building 'everything' server: {e}")
        finally:
            os.chdir(original_cwd)
            test_print("[BuildEverything] Build directory will be cleaned up.")
            # TemporaryDirectory cleans up automatically


# Use pytest_asyncio.fixture decorator
@pytest_asyncio.fixture(scope="function")
async def everything_mcp_server(
    built_everything_server_path: str,
) -> AsyncGenerator[MCPToolSet, None]:
    """Starts the pre-built 'everything' server using MCPToolSet."""
    command = "node"
    args = [built_everything_server_path]
    toolset = MCPToolSet(command=command, args=args)

    try:
        test_print(
            f"[Everything] Initializing MCPToolSet for {command} {args}..."
        )
        async with toolset as tools:
            test_print(
                f"[Everything] Context entered, yielded {len(tools)} tools."
            )
            if not toolset._worker or not toolset._worker._startup_success:
                pytest.fail(
                    "[Everything] MCP Worker failed during startup in fixture."
                )
            yield toolset
        test_print("[Everything] Context exited.")
    except Exception as e:
        test_print(f"[Everything] Error during setup/yield/context exit: {e}")
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                f"[Everything] Worker might still be alive after exception, attempting cleanup again."
            )
            toolset.cleanup()
        pytest.fail(f"Everything server fixture failed: {e}")
    finally:
        test_print("[Everything] Fixture teardown (finally block) reached.")
        if toolset._worker and toolset._worker.is_alive():
            test_print(
                "[Everything] WARNING: Worker thread still alive in fixture finally block!"
            )
        else:
            test_print(
                "[Everything] Worker confirmed stopped in fixture finally block."
            )

# src/crewai_mcp_toolbox/tests/test_chroma_integration.py
import asyncio
import os
from typing import Dict, List, Tuple

import openai

import pytest

# Import CrewAI components needed for the agent test
from crewai import Agent, Crew, CrewOutput, Process, Task
from crewai.tools import BaseTool

# Import only MCPToolSet from your package
from crewai_mcp_toolbox import MCPToolSet

# Import LLM_MODEL config from conftest
from tests.conftest import LLM_MODEL

# Ensure the OpenAI API key is picked up from the environment for the agent tests
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define sample data here OR ensure it's correctly imported/defined in conftest
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

# REMOVE the anext helper function


# This test uses the 'chroma_mcp_setup' fixture from conftest.py


@pytest.mark.asyncio
async def test_chroma_direct_tools(
    chroma_mcp_setup: Tuple[Dict[str, BaseTool], str],
):  # Use fixture directly
    """Test direct execution of some Chroma tools after setup."""
    # The fixture yields a tuple, so unpacking is correct here
    tools_dict, collection_name = chroma_mcp_setup

    print(f"\nTesting direct Chroma tools for collection: {collection_name}")

    # Test list_collections
    list_tool = tools_dict.get("chroma_list_collections")
    assert list_tool is not None
    result = list_tool._run()
    print(f"list_collections result: {result} ({type(result)})")

    is_expected_string = isinstance(result, str) and result == collection_name
    is_expected_list = False
    if isinstance(result, list):
        is_expected_list = any(
            isinstance(item, dict) and item.get("name") == collection_name
            for item in result
        )

    assert (
        is_expected_string or is_expected_list
    ), f"Expected collection name '{collection_name}' as string or in list, got: {result}"

    # Test get_collection_count
    count_tool = tools_dict.get("chroma_get_collection_count")
    assert count_tool is not None
    result_count = count_tool._run(collection_name=collection_name)
    print(f"get_collection_count result: {result_count}")
    assert (
        result_count == 5 or str(result_count) == "5"
    ), f"Expected count 5, got {result_count} ({type(result_count)})"

    # Test get_documents
    get_docs_tool = tools_dict.get("chroma_get_documents")
    assert get_docs_tool is not None
    include_param: List[str] = ["documents", "metadatas"]
    limit_param = "5"

    result_docs = get_docs_tool._run(
        collection_name=collection_name,
        include=include_param,
        limit=limit_param,
    )
    print(f"get_documents result: {result_docs}")
    assert isinstance(result_docs, dict), "get_documents should return a dict"
    assert (
        "documents" in result_docs
        and isinstance(result_docs["documents"], list)
        and len(result_docs["documents"]) == 5
    )
    assert (
        "metadatas" in result_docs
        and isinstance(result_docs["metadatas"], list)
        and len(result_docs["metadatas"]) == 5
    )
    assert (
        "ids" in result_docs
        and isinstance(result_docs.get("ids"), list)
        and len(result_docs.get("ids", [])) == 5
    )


# Skip this test if the LLM is not configured
@pytest.mark.skipif(
    LLM_MODEL is None,
    reason="LLM_MODEL not configured (e.g., OPENAI_API_KEY not set), skipping CrewAI agent test.",
)
@pytest.mark.asyncio
async def test_chroma_agent_workflow(
    chroma_mcp_setup: Tuple[Dict[str, BaseTool], str],
):  # Use fixture directly
    """Test a CrewAI agent using the loaded Chroma tools."""
    # Unpack the tuple yielded by the fixture
    tools_dict, collection_name = chroma_mcp_setup
    chroma_tools: List[BaseTool] = list(tools_dict.values())

    print(f"\nRunning CrewAI agent workflow for collection: {collection_name}")

    agent = Agent(
        role="Database Verifier",
        goal="Verify data in a Chroma collection using provided tools.",
        backstory="I check ChromaDB content via MCP.",
        tools=chroma_tools,
        verbose=True,
        llm=LLM_MODEL,
    )

    task_description = f"""
    1. Use the 'chroma_get_collection_count' tool to find out how many documents are in the collection named '{collection_name}'. Report this number clearly.
    2. Use the 'chroma_get_documents' tool to retrieve the first 5 documents and their metadatas from the '{collection_name}' collection. Ensure you request 'documents' and 'metadatas'.
    3. Based *only* on the results from the tools, state the exact number of documents found by the count tool. Then briefly summarize the topics covered in the retrieved documents based on their content.
    """
    task_config = {
        "description": task_description,
        "expected_output": f"Confirmation of the document count (which is 5) for '{collection_name}' and a brief summary mentioning Chroma/MCP based on the document content.",
        "agent": agent,
    }
    task = Task(config=task_config)

    crew = Crew(
        agents=[agent], tasks=[task], process=Process.sequential, verbose=True
    )

    crew_run_timeout = 180.0
    try:
        result: CrewOutput = await asyncio.wait_for(
            crew.kickoff_async(), timeout=crew_run_timeout
        )
        print("\nCrew execution completed.")
        print(f"Final Crew Result:\n{result.raw}")

        final_output = result.raw.lower()

        # --- MODIFIED ASSERTION ---
        # More robust check for the number 5 in the output
        contains_digit_5 = (
            " 5 " in final_output  # e.g., "found 5 documents"
            or " 5." in final_output  # e.g., "count is 5."
            or " is 5" in final_output  # e.g., "count is 5"
            or " contains 5" in final_output  # e.g., "collection contains 5"
            or " five "
            in final_output  # Keep checking for the word just in case
        )
        assert (
            contains_digit_5
        ), f"Crew output should explicitly mention '5' documents. Actual output: '{final_output}'"
        # --- END MODIFIED ASSERTION ---

        assert "chroma" in final_output, "Crew output should mention 'chroma'."
        assert (
            "mcp" in final_output or "protocol" in final_output
        ), "Crew output should mention 'mcp' or 'protocol'."
        assert " 10 " not in final_output
        assert " ten " not in final_output

    except asyncio.TimeoutError:
        pytest.fail(
            f"Crew execution timed out after {crew_run_timeout} seconds."
        )
    except Exception as crew_exc:
        pytest.fail(f"Crew execution failed: {crew_exc}")

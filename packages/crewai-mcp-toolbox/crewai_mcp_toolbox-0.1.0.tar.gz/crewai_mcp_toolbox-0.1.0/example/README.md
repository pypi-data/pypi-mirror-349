# Chroma MCP Crew Example

This directory contains `crew_chroma_mcp.py`, which demonstrates how to integrate a Chroma database with CrewAI using `crewai-mcp-toolbox`.

## How the Example Works

1. **MCP Tool Initialization** – `ChromaMCPCrew` starts the `chroma-mcp` server using `uvx` and loads the available tools via `MCPToolSet`.
2. **Agent Definition** – A single researcher agent is configured with the discovered tools and a default LLM model (`openai/gpt-4o-mini`).
3. **Task Creation** – `collection_query_task` describes how the agent should query a Chroma collection and summarize the results using the `chroma_query_collection` tool.
4. **Crew Assembly** – The `crew()` method gathers the agents and tasks into a `Crew` instance that can be executed sequentially.

## Running the Crew

```python
from example.crew_chroma_mcp import ChromaMCPCrew

with ChromaMCPCrew(data_dir="~/chroma_db") as crew_base:
    crew = crew_base.crew()
    result = crew.kickoff(
        tasks=[
            crew_base.collection_query_task(
                "my_collection", "search text", top_k=5
            )
        ]
    )
    print(result)
```

## Adapting for Your Own Crews

1. **Change the MCP server** – Modify the arguments passed to `MCPToolSet` in the `__init__` method if you want to connect to a different MCP server or data directory.
2. **Customize Agents** – Update `researcher_agent` or add new agents with `@agent` to match your roles and LLM configuration.
3. **Define New Tasks** – Create additional `@task` methods that use the loaded MCP tools to suit your workflow.
4. **Execute the Crew** – Use the `crew()` method to assemble your agents and tasks, then call `kickoff()` (or `kickoff_async()`) to run.

The example serves as a template – adjust the MCP tools, tasks, and agents as needed to build more complex workflows.
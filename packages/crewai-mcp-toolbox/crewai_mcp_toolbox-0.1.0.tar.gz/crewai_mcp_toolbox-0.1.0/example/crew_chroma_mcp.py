#!/usr/bin/env python
"""
Chroma MCP Crew for running vector database retrieval tasks.

This module provides a crew setup for executing search and retrieval tasks
using a Chroma database via the Model Context Protocol (MCP).
"""

import logging
import os
from typing import Any, Dict, List, Optional

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, tool

# Import the MCP integration
from crewai_mcp_toolbox import MCPToolSet

logger = logging.getLogger(__name__)


@CrewBase
class ChromaMCPCrew:
    """Crew for executing search and retrieval tasks using Chroma via MCP."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(
        self,
        data_dir: Optional[str] = None,
        log_file: Optional[str] = None,
        verbose: bool = True,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the ChromaMCPCrew with Chroma directory, logging options and MCP tools.

        Args:
            data_dir: Path to the Chroma database directory
            log_file: Path to the log file
            verbose: Whether to enable verbose logging
            config: Custom configuration for MCP timeouts and other settings
        """
        self.verbose = verbose
        self.log_file = log_file or "logs/chroma_mcp_crew.json"
        self.data_dir = data_dir or os.path.expanduser("~/chroma_db")

        # Create the directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)

        # Initialize the MCP toolset with the Chroma server
        self._mcp_toolset = MCPToolSet(
            command="uvx",
            args=[
                "chroma-mcp",
                "--client-type",
                "persistent",
                "--data-dir",
                self.data_dir,
            ],
            config=config,
        )

        # Tools will be initialized in initialize() or when using the context manager
        self._mcp_tools = []

        # Configure the researcher LLM
        self.researcher_llm = LLM(
            model="openai/gpt-4o-mini", temperature=0.2, max_tokens=4000
        )

    def initialize(self):
        """Initialize the MCP toolset and discover tools.

        Returns:
            The initialized crew instance for method chaining
        """
        self._mcp_tools = self._mcp_toolset.initialize()
        logger.info(
            f"Initialized MCP toolset with {len(self._mcp_tools)} tools"
        )
        return self

    @tool
    def mcp_tools(self):
        """Return all MCP tools discovered from the Chroma server."""
        return self._mcp_tools

    @agent
    def researcher_agent(self) -> Agent:
        """Create and return the researcher agent with MCP tools."""
        return Agent(
            config=self.agents_config.get("researcher_agent", {})
            or {
                "role": "Vector Database Researcher",
                "goal": "Efficiently retrieve and analyze information from Chroma vector database",
                "backstory": "I am a specialist in using vector databases to find relevant information.",
            },
            tools=self.mcp_tools(),
            memory=False,
            llm=self.researcher_llm,
            verbose=self.verbose,
        )

    @task
    def collection_query_task(
        self, collection_name: str, query: str, top_k: int = 5
    ) -> Task:
        """Create a task to query a specific Chroma collection.

        Args:
            collection_name: Name of the Chroma collection to query
            query: The search query text
            top_k: Number of results to return
        """
        return Task(
            config=self.tasks_config.get("collection_query_task", {})
            or {
                "description": f"""
                Your task is to search the '{collection_name}' collection in the Chroma database
                using the following query: "{query}"
                
                Return the top {top_k} most relevant results, and provide a concise summary
                of the information contained in those results.
                
                Use the chroma_query_collection tool to perform the search, and analyze the
                results thoroughly before presenting your findings.
                """,
                "expected_output": "A comprehensive analysis of the query results, with citations to the source documents.",
            },
            agent=self.researcher_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Create and return the Chroma MCP crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=self.verbose,
            memory=False,
            output_log_file=self.log_file,
        )

    def cleanup(self):
        """Clean up resources when done."""
        if hasattr(self, "_mcp_toolset"):
            self._mcp_toolset.cleanup()
            logger.info("Cleaned up MCP toolset resources")

    def __enter__(self):
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()

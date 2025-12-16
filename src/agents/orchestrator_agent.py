"""Orchestrator Agent - Coordinates the workflow using AutoGen."""

from autogen import AssistantAgent, GroupChat, GroupChatManager
from src.config.agent_config import get_llm_config


def create_orchestrator_agent() -> AssistantAgent:
    """Create and configure the Orchestrator Agent."""

    llm_config = get_llm_config()

    agent = AssistantAgent(
        name="orchestrator_agent",
        system_message="""You are the Orchestrator Agent that coordinates the entire video analysis workflow.
Your role is to:
1. Coordinate the workflow between specialized agents
2. Manage conversation flow and task delegation
3. Handle result aggregation from all agents
4. Ensure all three processing steps are completed:
   - Step 1: Parse the Planning Log (Log Parser Agent)
   - Step 2: Inspect the Video(s) (Video Analyzer Agent)
   - Step 3: Cross-check with Final Output (Test Output Parser Agent, Step Matcher Agent, Deviation Analyzer Agent)
5. Coordinate report generation (Report Generator Agent)

You delegate tasks to specialized agents and aggregate their results to produce the final deviation report.
Ensure all agents complete their tasks and communicate results effectively.""",
        llm_config=llm_config
    )

    return agent


def create_group_chat(agents: list) -> GroupChatManager:
    """Create a GroupChat with all agents."""
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=50
    )
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=get_llm_config()
    )
    return manager


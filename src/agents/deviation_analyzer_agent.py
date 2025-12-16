"""Deviation Analyzer Agent - Analyzes deviations using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config


def create_deviation_analyzer_agent() -> AssistantAgent:
    """Create and configure the Deviation Analyzer Agent."""

    llm_config = get_llm_config()

    agent = AssistantAgent(
        name="deviation_analyzer_agent",
        system_message="""You are a Deviation Analyzer Agent specialized in analyzing detected deviations.
Your role is to:
1. Perform final cross-checking and deviation analysis
2. Cross-check with Final Output (Step 3 requirement):
   - Validate consistency between planning log, video evidence, and test output
   - Check if test output assertions align with observed video actions
   - Identify discrepancies where test output claims differ from video evidence
   - Validate outcome alignment (expected vs actual results)
3. Determine deviation severity and context
4. Categorize deviations: skipped actions, altered actions, not visible, wrong context
5. Prepare comprehensive findings for Report Generator Agent

You receive match results from Step Matcher Agent and test output from Test Output Parser Agent.
Analyze the deviations, cross-reference with test output, and prepare findings for report generation.""",
        llm_config=llm_config
    )

    return agent


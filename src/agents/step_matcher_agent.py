"""Step Matcher Agent - Matches planned steps with video evidence using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config
from src.tools.step_matcher import (
    match_step_with_timeline,
    match_all_steps,
    categorize_deviation
)


def create_step_matcher_agent() -> AssistantAgent:
    """Create and configure the Step Matcher Agent."""

    llm_config = get_llm_config()

    # Define matching functions
    def match_step(planned_step: dict, timeline: list, threshold: float = 0.5) -> dict:
        """Match a single planned step with video timeline."""
        return match_step_with_timeline(planned_step, timeline, threshold)

    def match_all(planned_steps: list, timeline: list, threshold: float = 0.5) -> list:
        """Match all planned steps with video timeline."""
        return match_all_steps(planned_steps, timeline, threshold)

    def categorize(match_result: dict) -> str:
        """Categorize deviation type."""
        return categorize_deviation(match_result)

    # Register functions
    functions = [
        {
            "name": "match_step",
            "description": "Match a single planned step with actions in the video timeline",
            "parameters": {
                "type": "object",
                "properties": {
                    "planned_step": {
                        "type": "object",
                        "description": "Planned step dictionary with next_step and next_step_summary"
                    },
                    "timeline": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Timeline of observed actions from video"
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum similarity threshold (default: 0.5)",
                        "default": 0.5
                    }
                },
                "required": ["planned_step", "timeline"]
            }
        },
        {
            "name": "match_all",
            "description": "Match all planned steps with video timeline",
            "parameters": {
                "type": "object",
                "properties": {
                    "planned_steps": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of planned step dictionaries"
                    },
                    "timeline": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "Timeline of observed actions from video"
                    },
                    "threshold": {
                        "type": "number",
                        "description": "Minimum similarity threshold (default: 0.5)",
                        "default": 0.5
                    }
                },
                "required": ["planned_steps", "timeline"]
            }
        },
        {
            "name": "categorize",
            "description": "Categorize deviation type (observed, skipped, altered, not_visible)",
            "parameters": {
                "type": "object",
                "properties": {
                    "match_result": {
                        "type": "object",
                        "description": "Match result dictionary"
                    }
                },
                "required": ["match_result"]
            }
        }
    ]

    agent = AssistantAgent(
        name="step_matcher_agent",
        system_message="""You are a Step Matcher Agent specialized in matching planned steps with video evidence.
Your role is to:
1. Receive planned steps from Log Parser Agent
2. Receive observed actions timeline from Video Analyzer Agent
3. Receive test assertions from Test Output Parser Agent
4. Use semantic matching to compare planned actions with observed actions
5. For each planned step:
   - Search video timeline for matching action
   - Check if action is visibly executed in video
   - Verify action context matches (correct element, correct text, etc.)
6. Flag deviations (skipped, altered, not visible, wrong context)

Use the matching functions to compare planned steps with video evidence.
Return match results with similarity scores and deviation flags.""",
        llm_config={
            **llm_config,
            "functions": functions,
        },
        function_map={
            "match_step": match_step,
            "match_all": match_all,
            "categorize": categorize,
        }
    )

    return agent


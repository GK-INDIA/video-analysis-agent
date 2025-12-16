"""Log Parser Agent - Parses planning logs using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config
from src.tools.log_parser import parse_planning_log, extract_action_descriptions


def create_log_parser_agent() -> AssistantAgent:
    """Create and configure the Log Parser Agent."""

    llm_config = get_llm_config()

    # Define the log parser function for the agent to use
    def parse_log(log_path: str) -> dict:
        """Parse planning log from JSON file."""
        return parse_planning_log(log_path)

    def extract_actions(log_path: str) -> list:
        """Extract action descriptions from planning log."""
        parsed = parse_planning_log(log_path)
        return extract_action_descriptions(parsed["steps"])

    # Register functions
    functions = [
        {
            "name": "parse_log",
            "description": "Parse agent_inner_logs.json to extract planned steps, plan, and assertions",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_path": {
                        "type": "string",
                        "description": "Path to agent_inner_logs.json file"
                    }
                },
                "required": ["log_path"]
            }
        },
        {
            "name": "extract_actions",
            "description": "Extract action descriptions from planning log",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_path": {
                        "type": "string",
                        "description": "Path to agent_inner_logs.json file"
                    }
                },
                "required": ["log_path"]
            }
        }
    ]

    agent = AssistantAgent(
        name="log_parser_agent",
        system_message="""You are a Log Parser Agent specialized in parsing planning logs from Hercules test runs.
Your role is to:
1. Parse agent_inner_logs.json files to extract planned steps
2. Extract the plan, next_step, next_step_summary fields
3. Identify action descriptions (click, enter text, navigate, filter, etc.)
4. Create structured lists of planned actions with context

Use the parse_log and extract_actions functions to process planning logs.
Return structured data with planned steps, their summaries, and action descriptions.""",
        llm_config={
            **llm_config,
            "functions": functions,
        },
        function_map={
            "parse_log": parse_log,
            "extract_actions": extract_actions,
        }
    )

    return agent


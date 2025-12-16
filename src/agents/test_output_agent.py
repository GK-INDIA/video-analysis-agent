"""Test Output Parser Agent - Parses test results using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config
from src.tools.test_output_parser import parse_test_output


def create_test_output_agent() -> AssistantAgent:
    """Create and configure the Test Output Parser Agent."""

    llm_config = get_llm_config()

    # Define the test output parser function
    def parse_test_result(file_path: str) -> dict:
        """Parse test result file (XML or HTML)."""
        return parse_test_output(file_path)

    # Register functions
    functions = [
        {
            "name": "parse_test_result",
            "description": "Parse test_result.html or test_result.xml to extract test outcomes, failures, plan, and assertions",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to test_result.html or test_result.xml file"
                    }
                },
                "required": ["file_path"]
            }
        }
    ]

    agent = AssistantAgent(
        name="test_output_agent",
        system_message="""You are a Test Output Parser Agent specialized in parsing test results from Hercules test runs.
Your role is to:
1. Parse test_result.html or test_result.xml files
2. Extract test outcomes (passed/failed), failure messages, and assertions
3. Extract plan and step summaries from test output for cross-reference
4. Provide validation context for deviation analysis

Use the parse_test_result function to process test output files.
Return structured data with test outcomes, failures, plan, steps, and assertions.""",
        llm_config={
            **llm_config,
            "functions": functions,
        },
        function_map={
            "parse_test_result": parse_test_result,
        }
    )

    return agent


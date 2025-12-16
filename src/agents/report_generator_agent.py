"""Report Generator Agent - Generates deviation reports using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config
from src.tools.report_generator import (
    generate_deviation_report,
    save_report
)


def create_report_generator_agent() -> AssistantAgent:
    """Create and configure the Report Generator Agent."""

    llm_config = get_llm_config()

    # Define report generation functions
    def generate_report(match_results: list, test_output: dict = None, output_format: str = "markdown") -> str:
        """Generate deviation report from match results."""
        return generate_deviation_report(match_results, test_output, output_format)

    def save_report_file(report_content: str, output_path: str) -> dict:
        """Save report to file."""
        save_report(report_content, output_path)
        return {"status": "success", "output_path": output_path}

    # Register functions
    functions = [
        {
            "name": "generate_report",
            "description": "Generate deviation report from match results",
            "parameters": {
                "type": "object",
                "properties": {
                    "match_results": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "List of match result dictionaries"
                    },
                    "test_output": {
                        "type": "object",
                        "description": "Optional test output dictionary for cross-reference"
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "html"],
                        "description": "Output format (default: markdown)",
                        "default": "markdown"
                    }
                },
                "required": ["match_results"]
            }
        },
        {
            "name": "save_report_file",
            "description": "Save report content to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_content": {
                        "type": "string",
                        "description": "Report content as string"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where to save the report"
                    }
                },
                "required": ["report_content", "output_path"]
            }
        }
    ]

    agent = AssistantAgent(
        name="report_generator_agent",
        system_message="""You are a Report Generator Agent specialized in generating deviation reports.
Your role is to:
1. Generate final deviation report from deviation analysis findings
2. Format report with table structure:
   | Step Description | Result | Notes |
3. Include timestamps for deviations
4. Include summary statistics (total steps, deviations found)
5. Support both markdown and HTML output formats

Use the report generation functions to create comprehensive deviation reports.
The report should clearly show which steps were observed and which had deviations.""",
        llm_config={
            **llm_config,
            "functions": functions,
        },
        function_map={
            "generate_report": generate_report,
            "save_report_file": save_report_file,
        }
    )

    return agent


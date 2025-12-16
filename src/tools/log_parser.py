"""Parse planning logs from agent_inner_logs.json to extract planned steps."""

import json
from typing import List, Dict, Any
from pathlib import Path


def parse_planning_log(log_path: str) -> Dict[str, Any]:
    """
    Parse agent_inner_logs.json to extract planned steps.

    Args:
        log_path: Path to agent_inner_logs.json file

    Returns:
        Dictionary containing:
        - plan: Full plan as string
        - steps: List of step dictionaries with next_step, next_step_summary, etc.
        - assertions: List of assertion steps
    """
    with open(log_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    planner_agent = data.get("planner_agent", [])
    steps = []
    plan = None
    assertions = []

    for item in planner_agent:
        if item.get("role") == "assistant" and item.get("name") == "planner_agent":
            content = item.get("content", {})
            if isinstance(content, dict):
                # Extract plan
                if "plan" in content and plan is None:
                    plan = content["plan"]

                # Extract step information
                step_info = {
                    "next_step": content.get("next_step", ""),
                    "next_step_summary": content.get("next_step_summary", ""),
                    "terminate": content.get("terminate", "no"),
                    "is_assert": content.get("is_assert", False),
                    "assert_summary": content.get("assert_summary", ""),
                    "is_passed": content.get("is_passed", False),
                    "target_helper": content.get("target_helper", ""),
                    "final_response": content.get("final_response", ""),
                }

                if step_info["is_assert"]:
                    assertions.append(step_info)
                else:
                    steps.append(step_info)

    return {
        "plan": plan,
        "steps": steps,
        "assertions": assertions,
        "total_steps": len(steps),
        "total_assertions": len(assertions),
    }


def extract_action_descriptions(steps: List[Dict[str, Any]]) -> List[str]:
    """
    Extract action descriptions from steps.

    Args:
        steps: List of step dictionaries

    Returns:
        List of action description strings
    """
    actions = []
    for step in steps:
        summary = step.get("next_step_summary", "")
        if summary:
            actions.append(summary)
        else:
            # Extract action from next_step if summary is empty
            next_step = step.get("next_step", "")
            if next_step:
                # Try to extract the main action (first sentence or key phrase)
                actions.append(next_step.split('.')[0] if '.' in next_step else next_step[:100])
    return actions


if __name__ == "__main__":
    # Test the parser
    log_path = "data/agent_inner_logs.json"
    result = parse_planning_log(log_path)
    print(f"Plan: {result['plan']}")
    print(f"Total steps: {result['total_steps']}")
    print(f"Total assertions: {result['total_assertions']}")
    for i, step in enumerate(result['steps'], 1):
        print(f"\nStep {i}: {step['next_step_summary']}")


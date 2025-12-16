"""Match planned steps with video evidence."""

from typing import List, Dict, Any, Optional
import re


def semantic_match(planned_action: str, observed_action: str) -> float:
    """
    Calculate semantic similarity between planned and observed actions.

    Args:
        planned_action: Planned action description
        observed_action: Observed action description

    Returns:
        Similarity score between 0 and 1
    """
    planned_lower = planned_action.lower()
    observed_lower = observed_action.lower()

    # Extract key action words
    action_words = ["click", "enter", "type", "select", "navigate", "filter", "search", "submit", "open"]
    planned_actions = [word for word in action_words if word in planned_lower]
    observed_actions = [word for word in action_words if word in observed_lower]

    # Extract key objects (UI elements, text, etc.)
    planned_objects = extract_objects(planned_action)
    observed_objects = extract_objects(observed_action)

    # Calculate similarity
    action_match = len(set(planned_actions) & set(observed_actions)) / max(len(set(planned_actions) | set(observed_actions)), 1)
    object_match = len(set(planned_objects) & set(observed_objects)) / max(len(set(planned_objects) | set(observed_objects)), 1)

    # Weighted average
    similarity = (action_match * 0.6 + object_match * 0.4)

    return similarity


def extract_objects(text: str) -> List[str]:
    """Extract objects (UI elements, text content) from action description."""
    objects = []
    text_lower = text.lower()

    # Common UI elements
    ui_elements = ["search", "icon", "button", "input", "field", "filter", "menu", "link", "bar"]
    for element in ui_elements:
        if element in text_lower:
            objects.append(element)

    # Extract quoted text (likely specific values)
    quoted = re.findall(r'"([^"]*)"', text)
    objects.extend([q.lower() for q in quoted])

    # Extract capitalized words (likely proper nouns or labels)
    capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
    objects.extend([c.lower() for c in capitalized])

    return objects


def match_step_with_timeline(
    planned_step: Dict[str, Any],
    timeline: List[Dict[str, Any]],
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Match a planned step with actions in the video timeline.

    Args:
        planned_step: Planned step dictionary
        timeline: Timeline of observed actions
        threshold: Minimum similarity threshold

    Returns:
        Match result dictionary
    """
    planned_action = planned_step.get("next_step_summary", "") or planned_step.get("next_step", "")
    best_match = None
    best_score = 0.0
    matches = []

    for timeline_item in timeline:
        # Check actions
        for observed_action in timeline_item.get("actions", []):
            score = semantic_match(planned_action, observed_action)
            if score > best_score:
                best_score = score
                best_match = {
                    "timeline_item": timeline_item,
                    "observed_action": observed_action,
                    "score": score,
                    "timestamp": timeline_item.get("timestamp", 0),
                    "timestamp_formatted": timeline_item.get("timestamp_formatted", "00:00"),
                }

            if score >= threshold:
                matches.append({
                    "timeline_item": timeline_item,
                    "observed_action": observed_action,
                    "score": score,
                    "timestamp": timeline_item.get("timestamp", 0),
                    "timestamp_formatted": timeline_item.get("timestamp_formatted", "00:00"),
                })

        # Check UI elements and text content
        ui_elements = timeline_item.get("ui_elements", [])
        text_content = timeline_item.get("text_content", [])

        for element in ui_elements + text_content:
            score = semantic_match(planned_action, element)
            if score > best_score:
                best_score = score
                best_match = {
                    "timeline_item": timeline_item,
                    "observed_action": element,
                    "score": score,
                    "timestamp": timeline_item.get("timestamp", 0),
                    "timestamp_formatted": timeline_item.get("timestamp_formatted", "00:00"),
                }

    return {
        "planned_step": planned_step,
        "planned_action": planned_action,
        "best_match": best_match,
        "best_score": best_score,
        "all_matches": matches,
        "is_matched": best_score >= threshold,
        "result": "observed" if best_score >= threshold else "deviation",
    }


def match_all_steps(
    planned_steps: List[Dict[str, Any]],
    timeline: List[Dict[str, Any]],
    threshold: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Match all planned steps with video timeline.

    Args:
        planned_steps: List of planned step dictionaries
        timeline: Timeline of observed actions
        threshold: Minimum similarity threshold

    Returns:
        List of match results
    """
    results = []

    for step in planned_steps:
        match_result = match_step_with_timeline(step, timeline, threshold)
        results.append(match_result)

    return results


def categorize_deviation(match_result: Dict[str, Any]) -> str:
    """
    Categorize the type of deviation.

    Args:
        match_result: Match result dictionary

    Returns:
        Deviation category string
    """
    if match_result["is_matched"]:
        return "observed"

    best_score = match_result["best_score"]

    if best_score == 0.0:
        return "skipped"  # No match found
    elif best_score < 0.3:
        return "not_visible"  # Very low similarity
    else:
        return "altered"  # Partial match but context differs


if __name__ == "__main__":
    # Test the step matcher
    planned_step = {
        "next_step_summary": "Click the Search icon on the Wrangler homepage",
        "next_step": "Click search icon",
    }

    timeline = [
        {
            "timestamp": 5.0,
            "timestamp_formatted": "00:05",
            "actions": ["click search icon"],
            "ui_elements": ["search icon", "button"],
            "text_content": [],
        }
    ]

    result = match_step_with_timeline(planned_step, timeline)
    print(f"Match result: {result['result']}, Score: {result['best_score']}")


"""Detect actions in video frames using vision API."""

import base64
import io
import os
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from src.config.agent_config import get_vision_model

load_dotenv()


def encode_frame_to_base64(frame: np.ndarray) -> str:
    """Encode frame image to base64 string."""
    _, buffer = cv2.imencode(".jpg", frame)
    img_bytes = buffer.tobytes()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_base64


def analyze_frame_with_vision_api(
    frame: np.ndarray,
    prompt: str = "Describe what actions are visible in this screenshot. Focus on UI interactions like clicks, text input, navigation, filtering, etc. Also identify UI elements like buttons, input fields, icons, and any visible text.",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze a single frame using vision API.

    Args:
        frame: Frame image as numpy array
        prompt: Prompt for vision API
        api_key: API key (defaults to GROQ_API_KEY env var)
        base_url: Base URL (defaults to Groq API)

    Returns:
        Dictionary with analysis results
    """
    # Use Groq API configuration
    api_key = api_key or os.getenv("GROQ_API_KEY")
    base_url = base_url or "https://api.groq.com/openai/v1"

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Encode frame to base64
    img_base64 = encode_frame_to_base64(frame)

    try:
        # Get vision model from configuration
        vision_model = get_vision_model()

        # Call Groq Vision API using OpenAI-compatible format
        api_response = client.chat.completions.create(
            model=vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            },
                        },
                    ],
                }
            ],
        )

        # Extract description from API response
        description = api_response.choices[0].message.content

        # Process the description through extraction functions
        response = {
            "description": description,
            "ui_elements": extract_ui_elements(description),
            "actions": extract_actions(description),
            "text_content": extract_text_content(description),
        }

        return response

    except Exception as e:
        # Graceful error handling - return empty results with error message
        return {
            "error": str(e),
            "description": f"Error analyzing frame: {str(e)}",
            "ui_elements": [],
            "actions": [],
            "text_content": [],
            "notes": f"Vision API call failed: {str(e)}",
        }


def extract_ui_elements(description: str) -> List[str]:
    """Extract UI elements mentioned in description."""
    ui_keywords = [
        "button",
        "input",
        "field",
        "icon",
        "link",
        "menu",
        "dropdown",
        "filter",
        "search",
        "form",
    ]
    elements = []
    words = description.lower().split()
    for keyword in ui_keywords:
        if keyword in words:
            # Try to extract the full phrase
            idx = words.index(keyword)
            if idx > 0:
                phrase = " ".join(words[max(0, idx - 2) : idx + 2])
                elements.append(phrase)
    return elements


def extract_actions(description: str) -> List[str]:
    """Extract actions mentioned in description."""
    action_keywords = [
        "click",
        "enter",
        "type",
        "select",
        "navigate",
        "filter",
        "search",
        "submit",
        "open",
        "close",
    ]
    actions = []
    words = description.lower().split()
    for keyword in action_keywords:
        if keyword in words:
            idx = words.index(keyword)
            if idx > 0:
                phrase = " ".join(words[max(0, idx - 1) : idx + 3])
                actions.append(phrase)
    return actions


def extract_text_content(description: str) -> List[str]:
    """Extract text content mentioned in description."""
    # Look for quoted text or capitalized phrases
    import re

    # Find quoted text
    quoted = re.findall(r'"([^"]*)"', description)
    # Find capitalized phrases (likely UI labels)
    capitalized = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", description)
    return quoted + capitalized


def analyze_frames(
    frames: List[Dict[str, Any]], prompt: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Analyze multiple frames and build action timeline.

    Args:
        frames: List of frame dictionaries with 'frame' key
        prompt: Optional custom prompt

    Returns:
        List of analyzed frames with detected actions
    """
    analyzed_frames = []

    for frame_data in frames:
        frame = frame_data.get("frame")
        if frame is not None:
            analysis = analyze_frame_with_vision_api(frame, prompt)
            analyzed_frames.append(
                {
                    **frame_data,
                    "analysis": analysis,
                    "detected_actions": analysis.get("actions", []),
                    "ui_elements": analysis.get("ui_elements", []),
                    "text_content": analysis.get("text_content", []),
                }
            )
        else:
            analyzed_frames.append(
                {
                    **frame_data,
                    "analysis": {"error": "No frame data"},
                    "detected_actions": [],
                    "ui_elements": [],
                    "text_content": [],
                }
            )

    return analyzed_frames


def build_action_timeline(
    analyzed_frames: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Build timeline of observed actions from analyzed frames.

    Args:
        analyzed_frames: List of analyzed frame dictionaries

    Returns:
        Timeline of actions with timestamps
    """
    timeline = []

    for frame_data in analyzed_frames:
        timestamp = frame_data.get("timestamp", 0)
        timestamp_formatted = frame_data.get("timestamp_formatted", "00:00")
        actions = frame_data.get("detected_actions", [])
        ui_elements = frame_data.get("ui_elements", [])
        text_content = frame_data.get("text_content", [])
        description = frame_data.get("analysis", {}).get("description", "")

        if actions or ui_elements or text_content:
            timeline.append(
                {
                    "timestamp": timestamp,
                    "timestamp_formatted": timestamp_formatted,
                    "actions": actions,
                    "ui_elements": ui_elements,
                    "text_content": text_content,
                    "description": description,
                    "frame_number": frame_data.get("frame_number", 0),
                }
            )

    return timeline


if __name__ == "__main__":
    # Test the action detector
    print(
        "Action detector module loaded. Use analyze_frame_with_vision_api() to analyze frames."
    )

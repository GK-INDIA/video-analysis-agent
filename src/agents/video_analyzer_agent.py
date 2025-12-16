"""Video Analyzer Agent - Analyzes video evidence using AutoGen."""

from autogen import AssistantAgent
from src.config.agent_config import get_llm_config
from src.tools.video_analyzer import (
    extract_frames,
    extract_key_frames,
    process_multiple_videos,
    merge_video_timelines,
    get_video_info
)
from src.tools.action_detector import (
    analyze_frames,
    build_action_timeline
)


def create_video_analyzer_agent() -> AssistantAgent:
    """Create and configure the Video Analyzer Agent."""

    llm_config = get_llm_config()

    # Define video analysis functions
    def extract_video_frames(video_path: str, interval_seconds: float = 2.0) -> list:
        """Extract frames from video at regular intervals."""
        frames = extract_frames(video_path, interval_seconds)
        # Convert numpy arrays to serializable format
        return [
            {
                "frame_number": f["frame_number"],
                "timestamp": f["timestamp"],
                "timestamp_formatted": f["timestamp_formatted"],
            }
            for f in frames
        ]

    def analyze_video_frames(video_path: str, interval_seconds: float = 2.0) -> dict:
        """Extract and analyze frames from video."""
        frames = extract_frames(video_path, interval_seconds)
        analyzed = analyze_frames(frames)
        timeline = build_action_timeline(analyzed)
        return {
            "video_path": video_path,
            "frames_extracted": len(frames),
            "timeline": timeline,
        }

    def process_videos(video_paths: list, interval_seconds: float = 2.0) -> dict:
        """Process multiple videos and merge timelines."""
        video_frames = process_multiple_videos(video_paths, interval_seconds)
        unified_timeline = merge_video_timelines(video_frames)
        return {
            "videos_processed": len(video_frames),
            "unified_timeline": unified_timeline,
        }

    def get_video_metadata(video_path: str) -> dict:
        """Get video metadata."""
        return get_video_info(video_path)

    # Register functions
    functions = [
        {
            "name": "extract_video_frames",
            "description": "Extract frames from video at regular intervals",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to video file"
                    },
                    "interval_seconds": {
                        "type": "number",
                        "description": "Interval between frames in seconds (default: 2.0)",
                        "default": 2.0
                    }
                },
                "required": ["video_path"]
            }
        },
        {
            "name": "analyze_video_frames",
            "description": "Extract and analyze frames from video to build action timeline",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to video file"
                    },
                    "interval_seconds": {
                        "type": "number",
                        "description": "Interval between frames in seconds (default: 2.0)",
                        "default": 2.0
                    }
                },
                "required": ["video_path"]
            }
        },
        {
            "name": "process_videos",
            "description": "Process multiple videos and merge timelines for full coverage",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of video file paths"
                    },
                    "interval_seconds": {
                        "type": "number",
                        "description": "Interval between frames in seconds (default: 2.0)",
                        "default": 2.0
                    }
                },
                "required": ["video_paths"]
            }
        },
        {
            "name": "get_video_metadata",
            "description": "Get video metadata (fps, duration, dimensions)",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description": "Path to video file"
                    }
                },
                "required": ["video_path"]
            }
        }
    ]

    agent = AssistantAgent(
        name="video_analyzer_agent",
        system_message="""You are a Video Analyzer Agent specialized in analyzing video evidence from Hercules test runs.
Your role is to:
1. Extract frames from video files at regular intervals (1-2 seconds)
2. Extract key frames at scene changes/action boundaries
3. Use vision API to analyze frames for UI elements, text content, and visible actions
4. Build comprehensive timeline of observed actions
5. Handle multiple videos and coordinate coverage (merge timelines, handle overlapping actions)

Use the video analysis functions to process videos and build action timelines.
Return structured timelines with timestamps, detected actions, UI elements, and text content.""",
        llm_config={
            **llm_config,
            "functions": functions,
        },
        function_map={
            "extract_video_frames": extract_video_frames,
            "analyze_video_frames": analyze_video_frames,
            "process_videos": process_videos,
            "get_video_metadata": get_video_metadata,
        }
    )

    return agent


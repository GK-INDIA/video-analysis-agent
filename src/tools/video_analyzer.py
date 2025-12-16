"""Video processing and frame extraction."""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
import os


def extract_frames(video_path: str, interval_seconds: float = 2.0) -> List[Dict[str, Any]]:
    """
    Extract frames from video at regular intervals.

    Args:
        video_path: Path to video file
        interval_seconds: Interval between frames in seconds

    Returns:
        List of frame dictionaries with timestamp and frame data
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)
    frames = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps if fps > 0 else 0
            frames.append({
                "frame_number": frame_count,
                "timestamp": timestamp,
                "timestamp_formatted": format_timestamp(timestamp),
                "frame": frame,
            })

        frame_count += 1

    cap.release()
    return frames


def extract_key_frames(video_path: str, threshold: float = 30.0) -> List[Dict[str, Any]]:
    """
    Extract key frames at scene changes using frame difference.

    Args:
        video_path: Path to video file
        threshold: Threshold for detecting scene changes

    Returns:
        List of key frame dictionaries
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    prev_frame = None
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if prev_frame is not None:
            # Calculate frame difference
            gray_prev = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            gray_curr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(gray_prev, gray_curr)
            mean_diff = np.mean(diff)

            if mean_diff > threshold:
                timestamp = frame_count / fps if fps > 0 else 0
                frames.append({
                    "frame_number": frame_count,
                    "timestamp": timestamp,
                    "timestamp_formatted": format_timestamp(timestamp),
                    "frame": frame,
                    "diff_score": mean_diff,
                })
        else:
            # First frame
            timestamp = frame_count / fps if fps > 0 else 0
            frames.append({
                "frame_number": frame_count,
                "timestamp": timestamp,
                "timestamp_formatted": format_timestamp(timestamp),
                "frame": frame,
                "diff_score": 0.0,
            })

        prev_frame = frame.copy()
        frame_count += 1

    cap.release()
    return frames


def format_timestamp(seconds: float) -> str:
    """Format timestamp as MM:SS."""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


def save_frame(frame: np.ndarray, output_path: str) -> None:
    """Save frame to file."""
    cv2.imwrite(output_path, frame)


def process_multiple_videos(video_paths: List[str], interval_seconds: float = 2.0) -> Dict[str, List[Dict[str, Any]]]:
    """
    Process multiple videos and extract frames.

    Args:
        video_paths: List of video file paths
        interval_seconds: Interval between frames in seconds

    Returns:
        Dictionary mapping video paths to their extracted frames
    """
    all_frames = {}
    for video_path in video_paths:
        if os.path.exists(video_path):
            frames = extract_frames(video_path, interval_seconds)
            all_frames[video_path] = frames
        else:
            print(f"Warning: Video file not found: {video_path}")
    return all_frames


def merge_video_timelines(video_frames: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Merge frames from multiple videos into a unified timeline.

    Args:
        video_frames: Dictionary mapping video paths to their frames

    Returns:
        Unified timeline of frames sorted by timestamp
    """
    unified_timeline = []

    for video_path, frames in video_frames.items():
        for frame in frames:
            unified_timeline.append({
                **frame,
                "source_video": video_path,
            })

    # Sort by timestamp
    unified_timeline.sort(key=lambda x: x["timestamp"])

    return unified_timeline


def get_video_info(video_path: str) -> Dict[str, Any]:
    """
    Get video metadata.

    Args:
        video_path: Path to video file

    Returns:
        Dictionary with video information
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0

    cap.release()

    return {
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration": duration,
        "duration_formatted": format_timestamp(duration),
    }


if __name__ == "__main__":
    # Test the video analyzer
    video_path = "data/video.webm"
    if os.path.exists(video_path):
        info = get_video_info(video_path)
        print(f"Video Info: {info}")
        frames = extract_frames(video_path, interval_seconds=2.0)
        print(f"Extracted {len(frames)} frames")


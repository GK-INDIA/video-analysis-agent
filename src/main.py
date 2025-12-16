"""Main entry point for Video Analysis Agent."""

import argparse
import json
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.agents.log_parser_agent import create_log_parser_agent
from src.agents.video_analyzer_agent import create_video_analyzer_agent
from src.agents.test_output_agent import create_test_output_agent
from src.agents.step_matcher_agent import create_step_matcher_agent
from src.agents.deviation_analyzer_agent import create_deviation_analyzer_agent
from src.agents.report_generator_agent import create_report_generator_agent
from src.agents.orchestrator_agent import create_orchestrator_agent, create_group_chat

from src.tools.log_parser import parse_planning_log
from src.tools.test_output_parser import parse_test_output
from src.tools.video_analyzer import process_multiple_videos, merge_video_timelines
from src.tools.action_detector import analyze_frames, build_action_timeline
from src.tools.step_matcher import match_all_steps
from src.tools.report_generator import generate_deviation_report, save_report

console = Console()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Video Analysis Agent - Detect deviations between planned actions and video evidence"
    )
    parser.add_argument(
        "--log",
        type=str,
        default="data/agent_inner_logs.json",
        help="Path to agent_inner_logs.json file"
    )
    parser.add_argument(
        "--video",
        type=str,
        nargs="+",
        default=["data/video.webm"],
        help="Path(s) to video file(s) - can specify multiple videos"
    )
    parser.add_argument(
        "--test-output",
        type=str,
        default="data/test_result.xml",
        help="Path to test_result.html or test_result.xml file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output/deviation_report.md",
        help="Output path for deviation report"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "html"],
        default="markdown",
        help="Output format (markdown or html)"
    )
    parser.add_argument(
        "--use-agents",
        action="store_true",
        help="Use AutoGen agents for processing (experimental)"
    )

    args = parser.parse_args()

    console.print("[bold blue]Video Analysis Agent[/bold blue]")
    console.print("=" * 50)

    # Step 1: Parse Planning Log
    console.print("\n[bold]Step 1: Parsing Planning Log[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Parsing planning log...", total=None)
        try:
            planning_data = parse_planning_log(args.log)
            progress.update(task, completed=True)
            console.print(f"  ✓ Extracted {planning_data['total_steps']} planned steps")
            console.print(f"  ✓ Found {planning_data['total_assertions']} assertions")
        except Exception as e:
            console.print(f"  ✗ Error parsing planning log: {e}")
            return

    # Step 2: Analyze Video(s)
    console.print("\n[bold]Step 2: Analyzing Video(s)[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing video(s)...", total=None)
        try:
            # Process videos
            video_frames = process_multiple_videos(args.video, interval_seconds=2.0)

            # Analyze frames (placeholder - would use vision API in production)
            all_frames = []
            for video_path, frames in video_frames.items():
                analyzed = analyze_frames(frames)
                all_frames.extend(analyzed)

            # Build timeline
            timeline = build_action_timeline(all_frames)
            progress.update(task, completed=True)
            console.print(f"  ✓ Processed {len(video_frames)} video(s)")
            console.print(f"  ✓ Built timeline with {len(timeline)} action points")
        except Exception as e:
            console.print(f"  ✗ Error analyzing video: {e}")
            return

    # Step 3: Parse Test Output
    console.print("\n[bold]Step 3: Parsing Test Output[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Parsing test output...", total=None)
        try:
            test_output = parse_test_output(args.test_output)
            progress.update(task, completed=True)
            console.print(f"  ✓ Test outcome: {test_output['test_outcome']}")
            if test_output.get('failures'):
                console.print(f"  ✓ Found {len(test_output['failures'])} failure(s)")
        except Exception as e:
            console.print(f"  ✗ Error parsing test output: {e}")
            return

    # Step 4: Match Steps
    console.print("\n[bold]Step 4: Matching Steps with Video Evidence[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Matching steps...", total=None)
        try:
            match_results = match_all_steps(planning_data['steps'], timeline, threshold=0.5)
            progress.update(task, completed=True)
            observed = sum(1 for r in match_results if r.get("result") == "observed")
            deviations = len(match_results) - observed
            console.print(f"  ✓ Matched {len(match_results)} steps")
            console.print(f"  ✓ Observed: {observed}, Deviations: {deviations}")
        except Exception as e:
            console.print(f"  ✗ Error matching steps: {e}")
            return

    # Step 5: Generate Report
    console.print("\n[bold]Step 5: Generating Deviation Report[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Generating report...", total=None)
        try:
            report_content = generate_deviation_report(
                match_results,
                test_output,
                output_format=args.format
            )
            save_report(report_content, args.output)
            progress.update(task, completed=True)
            console.print(f"  ✓ Report generated: {args.output}")
        except Exception as e:
            console.print(f"  ✗ Error generating report: {e}")
            return

    # Summary
    console.print("\n[bold green]Analysis Complete![/bold green]")
    console.print(f"Report saved to: {args.output}")

    # Print summary
    total_steps = len(match_results)
    observed_count = sum(1 for r in match_results if r.get("result") == "observed")
    deviation_count = total_steps - observed_count

    console.print("\n[bold]Summary:[/bold]")
    console.print(f"  Total Steps: {total_steps}")
    console.print(f"  Observed: {observed_count}")
    console.print(f"  Deviations: {deviation_count}")


if __name__ == "__main__":
    main()


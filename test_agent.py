"""Comprehensive test script for Video Analysis Agent."""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_output.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def test_log_parser():
    """Test log parser functionality."""
    logger.info("=" * 60)
    logger.info("TEST 1: Log Parser")
    logger.info("=" * 60)

    try:
        from src.tools.log_parser import parse_planning_log, extract_action_descriptions

        log_path = "data/agent_inner_logs.json"
        logger.info(f"Parsing log file: {log_path}")

        result = parse_planning_log(log_path)

        logger.info(f"✓ Plan extracted: {len(result.get('plan', '').split('\\n'))} lines")
        logger.info(f"✓ Total steps: {result['total_steps']}")
        logger.info(f"✓ Total assertions: {result['total_assertions']}")

        # Log first few steps
        logger.info("\\nFirst 3 steps:")
        for i, step in enumerate(result['steps'][:3], 1):
            logger.info(f"  Step {i}: {step.get('next_step_summary', 'N/A')}")

        # Extract actions
        actions = extract_action_descriptions(result['steps'])
        logger.info(f"\\n✓ Extracted {len(actions)} action descriptions")
        logger.info(f"  Sample actions: {actions[:3]}")

        return True, result
    except Exception as e:
        logger.error(f"✗ Log parser test failed: {e}", exc_info=True)
        return False, None


def test_test_output_parser():
    """Test test output parser functionality."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 2: Test Output Parser")
    logger.info("=" * 60)

    try:
        from src.tools.test_output_parser import parse_test_output

        # Test XML parser
        xml_path = "data/test_result.xml"
        logger.info(f"Parsing XML file: {xml_path}")

        xml_result = parse_test_output(xml_path)
        logger.info(f"✓ Test outcome: {xml_result['test_outcome']}")
        logger.info(f"✓ Failures: {len(xml_result.get('failures', []))}")
        logger.info(f"✓ Plan extracted: {xml_result.get('plan') is not None}")
        logger.info(f"✓ Steps extracted: {len(xml_result.get('steps', []))}")

        if xml_result.get('failures'):
            logger.info(f"  Failure message: {xml_result['failures'][0].get('message', '')[:100]}")

        # Test HTML parser
        html_path = "data/test_result.html"
        logger.info(f"\\nParsing HTML file: {html_path}")

        html_result = parse_test_output(html_path)
        logger.info(f"✓ Test outcome: {html_result['test_outcome']}")
        logger.info(f"✓ Failures: {len(html_result.get('failures', []))}")
        logger.info(f"✓ Plan extracted: {html_result.get('plan') is not None}")

        return True, (xml_result, html_result)
    except Exception as e:
        logger.error(f"✗ Test output parser test failed: {e}", exc_info=True)
        return False, None


def test_video_analyzer():
    """Test video analyzer functionality."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 3: Video Analyzer")
    logger.info("=" * 60)

    try:
        from src.tools.video_analyzer import (
            extract_frames,
            get_video_info,
            process_multiple_videos,
            merge_video_timelines
        )

        video_path = "data/video.webm"
        logger.info(f"Analyzing video: {video_path}")

        # Get video info
        info = get_video_info(video_path)
        logger.info(f"✓ Video info:")
        logger.info(f"  Duration: {info['duration_formatted']}")
        logger.info(f"  FPS: {info['fps']:.2f}")
        logger.info(f"  Resolution: {info['width']}x{info['height']}")
        logger.info(f"  Total frames: {info['frame_count']}")

        # Extract frames
        logger.info("\\nExtracting frames (interval: 2 seconds)...")
        frames = extract_frames(video_path, interval_seconds=2.0)
        logger.info(f"✓ Extracted {len(frames)} frames")

        if frames:
            logger.info(f"  First frame timestamp: {frames[0]['timestamp_formatted']}")
            logger.info(f"  Last frame timestamp: {frames[-1]['timestamp_formatted']}")

        # Test multiple videos (same video for testing)
        logger.info("\\nTesting multiple video processing...")
        video_frames = process_multiple_videos([video_path], interval_seconds=2.0)
        logger.info(f"✓ Processed {len(video_frames)} video(s)")

        # Merge timelines
        unified_timeline = merge_video_timelines(video_frames)
        logger.info(f"✓ Unified timeline has {len(unified_timeline)} entries")

        return True, {"info": info, "frames": frames, "timeline": unified_timeline}
    except Exception as e:
        logger.error(f"✗ Video analyzer test failed: {e}", exc_info=True)
        return False, None


def test_action_detector():
    """Test action detector functionality."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 4: Action Detector")
    logger.info("=" * 60)

    try:
        from src.tools.action_detector import analyze_frames, build_action_timeline
        from src.tools.video_analyzer import extract_frames

        video_path = "data/video.webm"
        logger.info(f"Extracting frames for analysis: {video_path}")

        # Extract a few frames for testing
        frames = extract_frames(video_path, interval_seconds=5.0)  # Larger interval for faster testing
        logger.info(f"✓ Extracted {len(frames)} frames for analysis")

        if frames:
            # Analyze frames (this will use placeholder since vision API needs setup)
            logger.info("\\nAnalyzing frames...")
            analyzed = analyze_frames(frames[:3])  # Analyze first 3 frames only
            logger.info(f"✓ Analyzed {len(analyzed)} frames")

            # Build timeline
            timeline = build_action_timeline(analyzed)
            logger.info(f"✓ Built timeline with {len(timeline)} action points")

            if timeline:
                logger.info(f"  Sample timeline entry:")
                logger.info(f"    Timestamp: {timeline[0].get('timestamp_formatted', 'N/A')}")
                logger.info(f"    Actions: {timeline[0].get('actions', [])}")
        else:
            logger.warning("  No frames extracted, skipping analysis")
            timeline = []

        return True, {"timeline": timeline}
    except Exception as e:
        logger.error(f"✗ Action detector test failed: {e}", exc_info=True)
        return False, None


def test_step_matcher():
    """Test step matcher functionality."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 5: Step Matcher")
    logger.info("=" * 60)

    try:
        from src.tools.step_matcher import match_step_with_timeline, match_all_steps, semantic_match
        from src.tools.log_parser import parse_planning_log

        # Get planned steps
        log_path = "data/agent_inner_logs.json"
        planning_data = parse_planning_log(log_path)
        planned_steps = planning_data['steps']

        logger.info(f"✓ Loaded {len(planned_steps)} planned steps")

        # Create mock timeline (since video analysis might not have real actions)
        mock_timeline = [
            {
                "timestamp": 5.0,
                "timestamp_formatted": "00:05",
                "actions": ["navigate", "load page"],
                "ui_elements": ["search icon", "navigation bar"],
                "text_content": ["wrangler.in"],
            },
            {
                "timestamp": 12.0,
                "timestamp_formatted": "00:12",
                "actions": ["click search icon"],
                "ui_elements": ["search icon", "search bar"],
                "text_content": [],
            },
            {
                "timestamp": 18.0,
                "timestamp_formatted": "00:18",
                "actions": ["enter text", "type"],
                "ui_elements": ["search bar", "input field"],
                "text_content": ["Rainbow sweater"],
            },
        ]

        logger.info(f"✓ Created mock timeline with {len(mock_timeline)} entries")

        # Test semantic matching
        logger.info("\\nTesting semantic matching...")
        planned_action = planned_steps[0].get('next_step_summary', '') or planned_steps[0].get('next_step', '')
        observed_action = "navigate to wrangler.in"
        similarity = semantic_match(planned_action, observed_action)
        logger.info(f"✓ Semantic match score: {similarity:.2f}")
        logger.info(f"  Planned: {planned_action[:60]}...")
        logger.info(f"  Observed: {observed_action}")

        # Test matching a step
        logger.info("\\nTesting step matching...")
        match_result = match_step_with_timeline(planned_steps[0], mock_timeline, threshold=0.5)
        logger.info(f"✓ Match result: {match_result['result']}")
        logger.info(f"  Best score: {match_result['best_score']:.2f}")
        logger.info(f"  Is matched: {match_result['is_matched']}")

        # Test matching all steps
        logger.info("\\nTesting matching all steps...")
        all_matches = match_all_steps(planned_steps[:3], mock_timeline, threshold=0.5)
        logger.info(f"✓ Matched {len(all_matches)} steps")
        observed_count = sum(1 for r in all_matches if r.get("result") == "observed")
        logger.info(f"  Observed: {observed_count}, Deviations: {len(all_matches) - observed_count}")

        return True, {"matches": all_matches}
    except Exception as e:
        logger.error(f"✗ Step matcher test failed: {e}", exc_info=True)
        return False, None


def test_report_generator():
    """Test report generator functionality."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 6: Report Generator")
    logger.info("=" * 60)

    try:
        from src.tools.report_generator import generate_deviation_report, save_report
        from src.tools.step_matcher import match_all_steps
        from src.tools.log_parser import parse_planning_log
        from src.tools.test_output_parser import parse_test_output

        # Get data
        log_path = "data/agent_inner_logs.json"
        test_output_path = "data/test_result.xml"

        planning_data = parse_planning_log(log_path)
        test_output = parse_test_output(test_output_path)

        # Create mock timeline
        mock_timeline = [
            {
                "timestamp": 5.0,
                "timestamp_formatted": "00:05",
                "actions": ["navigate"],
                "ui_elements": ["search icon"],
                "text_content": [],
            },
            {
                "timestamp": 12.0,
                "timestamp_formatted": "00:12",
                "actions": ["click search"],
                "ui_elements": ["search icon"],
                "text_content": [],
            },
        ]

        # Match steps
        match_results = match_all_steps(planning_data['steps'], mock_timeline, threshold=0.5)

        logger.info(f"✓ Generated {len(match_results)} match results")

        # Generate markdown report
        logger.info("\\nGenerating markdown report...")
        md_report = generate_deviation_report(match_results, test_output, output_format="markdown")
        logger.info(f"✓ Markdown report generated ({len(md_report)} characters)")
        logger.info(f"  Preview: {md_report[:200]}...")

        # Save report
        output_path = "test_output/test_report.md"
        Path("test_output").mkdir(exist_ok=True)
        save_report(md_report, output_path)
        logger.info(f"✓ Report saved to: {output_path}")

        # Generate HTML report
        logger.info("\\nGenerating HTML report...")
        html_report = generate_deviation_report(match_results, test_output, output_format="html")
        logger.info(f"✓ HTML report generated ({len(html_report)} characters)")

        html_output_path = "test_output/test_report.html"
        save_report(html_report, html_output_path)
        logger.info(f"✓ HTML report saved to: {html_output_path}")

        return True, {"md_report": md_report, "html_report": html_report}
    except Exception as e:
        logger.error(f"✗ Report generator test failed: {e}", exc_info=True)
        return False, None


def test_full_workflow():
    """Test the full workflow end-to-end."""
    logger.info("\\n" + "=" * 60)
    logger.info("TEST 7: Full Workflow")
    logger.info("=" * 60)

    try:
        from src.tools.log_parser import parse_planning_log
        from src.tools.test_output_parser import parse_test_output
        from src.tools.video_analyzer import extract_frames
        from src.tools.action_detector import analyze_frames, build_action_timeline
        from src.tools.step_matcher import match_all_steps
        from src.tools.report_generator import generate_deviation_report, save_report

        # Step 1: Parse planning log
        logger.info("Step 1: Parsing planning log...")
        planning_data = parse_planning_log("data/agent_inner_logs.json")
        logger.info(f"  ✓ Extracted {planning_data['total_steps']} steps")

        # Step 2: Parse test output
        logger.info("Step 2: Parsing test output...")
        test_output = parse_test_output("data/test_result.xml")
        logger.info(f"  ✓ Test outcome: {test_output['test_outcome']}")

        # Step 3: Analyze video (limited frames for testing)
        logger.info("Step 3: Analyzing video...")
        frames = extract_frames("data/video.webm", interval_seconds=5.0)
        logger.info(f"  ✓ Extracted {len(frames)} frames")

        # Analyze frames
        analyzed = analyze_frames(frames[:5])  # Analyze first 5 frames
        timeline = build_action_timeline(analyzed)
        logger.info(f"  ✓ Built timeline with {len(timeline)} action points")

        # Step 4: Match steps
        logger.info("Step 4: Matching steps...")
        match_results = match_all_steps(planning_data['steps'], timeline, threshold=0.5)
        observed = sum(1 for r in match_results if r.get("result") == "observed")
        deviations = len(match_results) - observed
        logger.info(f"  ✓ Observed: {observed}, Deviations: {deviations}")

        # Step 5: Generate report
        logger.info("Step 5: Generating report...")
        report = generate_deviation_report(match_results, test_output, output_format="markdown")
        output_path = "test_output/full_workflow_report.md"
        Path("test_output").mkdir(exist_ok=True)
        save_report(report, output_path)
        logger.info(f"  ✓ Report saved to: {output_path}")

        # Summary
        logger.info("\\n" + "=" * 60)
        logger.info("WORKFLOW SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total Steps: {len(match_results)}")
        logger.info(f"Observed: {observed}")
        logger.info(f"Deviations: {deviations}")
        logger.info(f"Report: {output_path}")

        return True, {"match_results": match_results, "report_path": output_path}
    except Exception as e:
        logger.error(f"✗ Full workflow test failed: {e}", exc_info=True)
        return False, None


def main():
    """Run all tests."""
    logger.info("\\n" + "=" * 60)
    logger.info("VIDEO ANALYSIS AGENT - COMPREHENSIVE TEST SUITE")
    logger.info("=" * 60)
    logger.info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("\\n")

    results = {}

    # Run all tests
    results['log_parser'] = test_log_parser()
    results['test_output_parser'] = test_test_output_parser()
    results['video_analyzer'] = test_video_analyzer()
    results['action_detector'] = test_action_detector()
    results['step_matcher'] = test_step_matcher()
    results['report_generator'] = test_report_generator()
    results['full_workflow'] = test_full_workflow()

    # Summary
    logger.info("\\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)

    passed = sum(1 for success, _ in results.values() if success)
    total = len(results)

    for test_name, (success, _) in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        logger.info(f"{test_name:30s} {status}")

    logger.info("\\n" + "-" * 60)
    logger.info(f"Total: {passed}/{total} tests passed")
    logger.info(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("\\nLog file saved to: test_output.log")

    if passed == total:
        logger.info("\\n🎉 All tests passed!")
        return 0
    else:
        logger.error(f"\\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())


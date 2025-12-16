"""Generate deviation report."""

from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime


def generate_deviation_report(
    match_results: List[Dict[str, Any]],
    test_output: Optional[Dict[str, Any]] = None,
    output_format: str = "markdown"
) -> str:
    """
    Generate deviation report from match results.

    Args:
        match_results: List of match result dictionaries
        test_output: Optional test output dictionary for cross-reference
        output_format: Output format ("markdown" or "html")

    Returns:
        Report content as string
    """
    if output_format == "html":
        return generate_html_report(match_results, test_output)
    else:
        return generate_markdown_report(match_results, test_output)


def generate_markdown_report(
    match_results: List[Dict[str, Any]],
    test_output: Optional[Dict[str, Any]] = None
) -> str:
    """Generate markdown deviation report."""
    report_lines = []

    # Header
    report_lines.append("# Deviation Report")
    report_lines.append("")
    report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Summary
    total_steps = len(match_results)
    observed_count = sum(1 for r in match_results if r.get("result") == "observed")
    deviation_count = total_steps - observed_count

    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- **Total Steps:** {total_steps}")
    report_lines.append(f"- **Observed:** {observed_count}")
    report_lines.append(f"- **Deviations:** {deviation_count}")
    report_lines.append("")

    # Test output cross-reference
    if test_output:
        report_lines.append("## Test Output Cross-Reference")
        report_lines.append("")
        report_lines.append(f"- **Test Outcome:** {test_output.get('test_outcome', 'unknown')}")
        if test_output.get("failures"):
            report_lines.append(f"- **Failures:** {len(test_output['failures'])}")
            for failure in test_output["failures"]:
                report_lines.append(f"  - {failure.get('message', '')[:100]}")
        report_lines.append("")

    # Detailed Results
    report_lines.append("## Detailed Results")
    report_lines.append("")
    report_lines.append("| Step Description | Result | Notes |")
    report_lines.append("|------------------|--------|-------|")

    for i, result in enumerate(match_results, 1):
        planned_action = result.get("planned_action", f"Step {i}")
        match_status = result.get("result", "unknown")

        # Format result symbol
        if match_status == "observed":
            result_symbol = "☑ Observed"
        else:
            result_symbol = "✗ Deviation"

        # Get notes
        notes = "-"
        if not result.get("is_matched"):
            best_match = result.get("best_match")
            if best_match:
                notes = f"Partial match (score: {best_match['score']:.2f})"
            else:
                deviation_type = categorize_deviation_type(result)
                notes = f"Step {deviation_type} in video"
        elif result.get("best_match"):
            timestamp = result["best_match"].get("timestamp_formatted", "")
            if timestamp:
                notes = f"Observed at {timestamp}"

        # Truncate long descriptions
        if len(planned_action) > 60:
            planned_action = planned_action[:57] + "..."

        report_lines.append(f"| {planned_action} | {result_symbol} | {notes} |")

    report_lines.append("")

    # Deviations Detail
    deviations = [r for r in match_results if r.get("result") != "observed"]
    if deviations:
        report_lines.append("## Deviations Detail")
        report_lines.append("")
        for i, deviation in enumerate(deviations, 1):
            planned_action = deviation.get("planned_action", f"Step {i}")
            deviation_type = categorize_deviation_type(deviation)
            report_lines.append(f"### Deviation {i}: {deviation_type}")
            report_lines.append("")
            report_lines.append(f"**Planned Action:** {planned_action}")
            report_lines.append("")
            if deviation.get("best_match"):
                best_match = deviation["best_match"]
                report_lines.append(f"**Closest Match:** {best_match.get('observed_action', 'N/A')}")
                report_lines.append(f"**Similarity Score:** {best_match.get('score', 0):.2f}")
            report_lines.append("")

    return "\n".join(report_lines)


def generate_html_report(
    match_results: List[Dict[str, Any]],
    test_output: Optional[Dict[str, Any]] = None
) -> str:
    """Generate HTML deviation report."""
    html_lines = []

    html_lines.append("<!DOCTYPE html>")
    html_lines.append("<html>")
    html_lines.append("<head>")
    html_lines.append('<meta charset="UTF-8">')
    html_lines.append("<title>Deviation Report</title>")
    html_lines.append("<style>")
    html_lines.append("body { font-family: Arial, sans-serif; margin: 20px; }")
    html_lines.append("table { border-collapse: collapse; width: 100%; margin: 20px 0; }")
    html_lines.append("th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }")
    html_lines.append("th { background-color: #f2f2f2; }")
    html_lines.append(".observed { color: green; }")
    html_lines.append(".deviation { color: red; }")
    html_lines.append("</style>")
    html_lines.append("</head>")
    html_lines.append("<body>")

    html_lines.append("<h1>Deviation Report</h1>")
    html_lines.append(f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>")

    # Summary
    total_steps = len(match_results)
    observed_count = sum(1 for r in match_results if r.get("result") == "observed")
    deviation_count = total_steps - observed_count

    html_lines.append("<h2>Summary</h2>")
    html_lines.append("<ul>")
    html_lines.append(f"<li><strong>Total Steps:</strong> {total_steps}</li>")
    html_lines.append(f"<li><strong>Observed:</strong> {observed_count}</li>")
    html_lines.append(f"<li><strong>Deviations:</strong> {deviation_count}</li>")
    html_lines.append("</ul>")

    # Table
    html_lines.append("<h2>Detailed Results</h2>")
    html_lines.append("<table>")
    html_lines.append("<tr><th>Step Description</th><th>Result</th><th>Notes</th></tr>")

    for i, result in enumerate(match_results, 1):
        planned_action = result.get("planned_action", f"Step {i}")
        match_status = result.get("result", "unknown")

        if match_status == "observed":
            result_symbol = "☑ Observed"
            result_class = "observed"
        else:
            result_symbol = "✗ Deviation"
            result_class = "deviation"

        notes = "-"
        if not result.get("is_matched"):
            best_match = result.get("best_match")
            if best_match:
                notes = f"Partial match (score: {best_match['score']:.2f})"
            else:
                deviation_type = categorize_deviation_type(result)
                notes = f"Step {deviation_type} in video"
        elif result.get("best_match"):
            timestamp = result["best_match"].get("timestamp_formatted", "")
            if timestamp:
                notes = f"Observed at {timestamp}"

        # Escape HTML
        planned_action = planned_action.replace("<", "&lt;").replace(">", "&gt;")
        notes = notes.replace("<", "&lt;").replace(">", "&gt;")

        html_lines.append(f"<tr class='{result_class}'>")
        html_lines.append(f"<td>{planned_action}</td>")
        html_lines.append(f"<td>{result_symbol}</td>")
        html_lines.append(f"<td>{notes}</td>")
        html_lines.append("</tr>")

    html_lines.append("</table>")
    html_lines.append("</body>")
    html_lines.append("</html>")

    return "\n".join(html_lines)


def save_report(report_content: str, output_path: str) -> None:
    """Save report to file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report_content)


def categorize_deviation_type(match_result: Dict[str, Any]) -> str:
    """Categorize deviation type."""
    if match_result.get("is_matched"):
        return "observed"

    best_score = match_result.get("best_score", 0.0)

    if best_score == 0.0:
        return "skipped"
    elif best_score < 0.3:
        return "not_visible"
    else:
        return "altered"


if __name__ == "__main__":
    # Test the report generator
    test_results = [
        {
            "planned_action": "Click the Search icon",
            "result": "observed",
            "is_matched": True,
            "best_match": {"timestamp_formatted": "00:05", "score": 0.9},
        },
        {
            "planned_action": "Enter password",
            "result": "deviation",
            "is_matched": False,
            "best_score": 0.0,
        },
    ]

    report = generate_markdown_report(test_results)
    print(report)


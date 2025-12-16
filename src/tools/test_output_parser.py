"""Parse test results from test_result.html or test_result.xml."""

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
from pathlib import Path


def parse_test_output_xml(xml_path: str) -> Dict[str, Any]:
    """
    Parse test_result.xml to extract test outcomes.

    Args:
        xml_path: Path to test_result.xml file

    Returns:
        Dictionary containing test results, plan, steps, and assertions
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    result = {
        "test_outcome": "unknown",
        "failures": [],
        "plan": None,
        "steps": [],
        "assertions": [],
        "properties": {},
    }

    # Parse testsuite
    testsuite = root.find("testsuite")
    if testsuite is not None:
        result["test_outcome"] = "failed" if int(testsuite.get("failures", 0)) > 0 else "passed"
        result["total_tests"] = int(testsuite.get("tests", 0))
        result["failures_count"] = int(testsuite.get("failures", 0))

        # Parse testcase
        testcase = testsuite.find("testcase")
        if testcase is not None:
            # Check for failure
            failure = testcase.find("failure")
            if failure is not None:
                result["failures"].append({
                    "message": failure.get("message", ""),
                    "text": failure.text if failure.text else "",
                })

            # Parse properties
            properties = testcase.find("properties")
            if properties is not None:
                for prop in properties.findall("property"):
                    name = prop.get("name", "")
                    value = prop.get("value", "")
                    result["properties"][name] = value

                    # Extract plan and steps from properties
                    if name == "plan":
                        result["plan"] = value
                        # Parse plan into steps
                        if value:
                            result["steps"] = parse_plan_from_text(value)
                    elif name == "next_step":
                        result["steps"].append({
                            "next_step": value,
                            "summary": result["properties"].get("next_step_summary", ""),
                        })
                    elif name == "assert_summary" or "assert" in name.lower():
                        result["assertions"].append({
                            "assert_summary": value,
                            "expected": extract_expected_from_assertion(value),
                            "actual": extract_actual_from_assertion(value),
                        })

    return result


def parse_test_output_html(html_path: str) -> Dict[str, Any]:
    """
    Parse test_result.html to extract test outcomes.

    Args:
        html_path: Path to test_result.html file

    Returns:
        Dictionary containing test results, plan, steps, and assertions
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    result = {
        "test_outcome": "unknown",
        "failures": [],
        "plan": None,
        "steps": [],
        "assertions": [],
        "properties": {},
    }

    # Find test outcome
    outcome_elem = soup.find(class_="outcome-failed")
    if outcome_elem:
        result["test_outcome"] = "failed"
    else:
        outcome_elem = soup.find(class_="outcome-passed")
        if outcome_elem:
            result["test_outcome"] = "passed"

    # Find failure message
    failure_elem = soup.find("th", string="Failed")
    if failure_elem:
        failure_td = failure_elem.find_next_sibling("td")
        if failure_td:
            result["failures"].append({
                "message": failure_td.get_text(strip=True),
            })

    # Extract plan and steps from properties table
    prop_tables = soup.find_all("table", class_="proplist")
    for table in prop_tables:
        rows = table.find_all("tr")
        for row in rows:
            th = row.find("th")
            td = row.find("td")
            if th and td:
                name = th.get_text(strip=True)
                value = td.get_text(strip=True)
                result["properties"][name] = value

                if name == "plan":
                    result["plan"] = value
                    result["steps"] = parse_plan_from_text(value)
                elif name == "next_step":
                    result["steps"].append({
                        "next_step": value,
                        "summary": result["properties"].get("next_step_summary", ""),
                    })
                elif "assert" in name.lower():
                    result["assertions"].append({
                        "assert_summary": value,
                        "expected": extract_expected_from_assertion(value),
                        "actual": extract_actual_from_assertion(value),
                    })

    return result


def parse_plan_from_text(plan_text: str) -> List[Dict[str, str]]:
    """Parse plan text into individual steps."""
    steps = []
    lines = plan_text.split('\n')
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering
            step_text = line.split('.', 1)[-1].strip() if '.' in line else line[1:].strip()
            if step_text:
                steps.append({
                    "description": step_text,
                    "step_number": len(steps) + 1,
                })
    return steps


def extract_expected_from_assertion(assertion_text: str) -> Optional[str]:
    """Extract expected result from assertion text."""
    if "EXPECTED RESULT:" in assertion_text:
        parts = assertion_text.split("EXPECTED RESULT:")
        if len(parts) > 1:
            expected = parts[1].split("ACTUAL RESULT:")[0].strip()
            return expected
    return None


def extract_actual_from_assertion(assertion_text: str) -> Optional[str]:
    """Extract actual result from assertion text."""
    if "ACTUAL RESULT:" in assertion_text:
        parts = assertion_text.split("ACTUAL RESULT:")
        if len(parts) > 1:
            actual = parts[1].strip()
            return actual
    return None


def parse_test_output(file_path: str) -> Dict[str, Any]:
    """
    Parse test output file (XML or HTML).

    Args:
        file_path: Path to test_result.xml or test_result.html

    Returns:
        Dictionary containing parsed test results
    """
    path = Path(file_path)
    if path.suffix == '.xml':
        return parse_test_output_xml(file_path)
    elif path.suffix == '.html':
        return parse_test_output_html(file_path)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


if __name__ == "__main__":
    # Test the parser
    xml_path = "data/test_result.xml"
    result = parse_test_output(xml_path)
    print(f"Test Outcome: {result['test_outcome']}")
    print(f"Plan: {result['plan']}")
    print(f"Failures: {result['failures']}")


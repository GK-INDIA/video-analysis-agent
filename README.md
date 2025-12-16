# Video Analysis Agent

A multi-agent system built with AutoGen that evaluates whether a Hercules test run was executed as planned by comparing planning logs, video evidence, and test outputs to detect deviations.

## Overview

The Video Analysis Agent analyzes three types of inputs:
1. **Planning Log** - The agent's intended step-by-step actions
2. **Video Evidence** - Actual execution captured in video(s)
3. **Test Output** - Final test results and assertions

The agent detects if claimed actions are visibly executed in the video and flags any deviations (skipped, altered, or not visible actions).

## Features

- ✅ Parse planning logs from `agent_inner_logs.json`
- ✅ Analyze video evidence (supports multiple videos)
- ✅ Cross-check with test output (`test_result.html` or `test_result.xml`)
- ✅ Semantic matching between planned and observed actions
- ✅ Generate comprehensive deviation reports (Markdown or HTML)
- ✅ Multi-agent architecture using AutoGen framework
- ✅ Powered by Groq API (GPT-OSS-120B model)

## Installation

### Prerequisites

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd video-analysis-agent
   ```

2. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Groq API key
   ```

   The `.env` file should contain:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

   **Note:** Replace `your_groq_api_key_here` with your actual Groq API key. You can obtain an API key from [Groq Console](https://console.groq.com/).

## How to Run the Agent

### Basic Usage

Run the agent with default input files from the `data/` directory:

```bash
uv run python main.py
```

### Custom Input Files

Specify custom input files:

```bash
uv run python main.py \
  --log data/agent_inner_logs.json \
  --video data/video.webm \
  --test-output data/test_result.xml \
  --output output/deviation_report.md
```

### Multiple Videos

Process multiple videos for full coverage:

```bash
uv run python main.py \
  --video data/video1.webm data/video2.webm data/video3.webm
```

### Output Format

Generate HTML report instead of Markdown:

```bash
uv run python main.py --format html --output output/deviation_report.html
```

### Command-Line Options

```
--log PATH              Path to agent_inner_logs.json (default: data/agent_inner_logs.json)
--video PATH [PATH ...] Path(s) to video file(s) - can specify multiple (default: data/video.webm)
--test-output PATH      Path to test_result.html or test_result.xml (default: data/test_result.xml)
--output PATH           Output path for deviation report (default: output/deviation_report.md)
--format FORMAT         Output format: markdown or html (default: markdown)
--use-agents            Use AutoGen agents for processing (experimental)
```

## Where Output is Saved

By default, the deviation report is saved to:
- **Default location:** `output/deviation_report.md`
- **Custom location:** Specify with `--output` flag

The output directory is created automatically if it doesn't exist.

### Output Formats

- **Markdown** (`.md`): Human-readable markdown format with tables
- **HTML** (`.html`): Formatted HTML report with styling

### Output File Naming Convention

- Default: `deviation_report.md` or `deviation_report.html`
- Timestamped: You can customize the filename in the `--output` argument
- Example: `output/report_2025-01-15_14-30-00.md`

## Sample Inputs and Expected Outputs

### Input File Formats

#### 1. Planning Log (`agent_inner_logs.json`)

The planning log contains the agent's intended steps in JSON format:

```json
{
  "planner_agent": [
    {
      "content": {
        "plan": "1. Navigate to the Wrangler website...\n2. Click on Search icon...",
        "next_step": "Navigate to the URL https://wrangler.in...",
        "next_step_summary": "Navigate to https://wrangler.in and validate homepage load",
        "terminate": "no",
        "is_assert": false
      },
      "role": "assistant",
      "name": "planner_agent"
    }
  ]
}
```

**Expected Structure:**
- `plan`: Full plan as numbered list
- `next_step`: Detailed step description
- `next_step_summary`: Brief step summary
- `is_assert`: Boolean indicating if this is an assertion
- `terminate`: "yes" or "no" indicating if test should terminate

#### 2. Video File (`video.webm`)

- Format: WebM, MP4, or other formats supported by OpenCV
- Content: Screen recording of the test execution
- Multiple videos: Supported for full coverage

#### 3. Test Output (`test_result.xml` or `test_result.html`)

**XML Format:**
```xml
<testsuite>
  <testcase>
    <failure message="EXPECTED RESULT: ... ACTUAL RESULT: ..."/>
    <properties>
      <property name="plan" value="1. Navigate..."/>
      <property name="next_step" value="..."/>
    </properties>
  </testcase>
</testsuite>
```

**HTML Format:**
- JUnit-style HTML report
- Contains test outcome, failures, plan, and step information

### Expected Output Format

The deviation report follows this structure:

```markdown
# Deviation Report

Generated: 2025-01-15 14:30:00

## Summary

- **Total Steps:** 10
- **Observed:** 8
- **Deviations:** 2

## Detailed Results

| Step Description | Result | Notes |
|------------------|--------|-------|
| Navigate to https://wrangler.in | ☑ Observed | Observed at 00:05 |
| Click the Search icon | ☑ Observed | Observed at 00:12 |
| Enter 'Rainbow sweater' | ☑ Observed | Observed at 00:18 |
| Select 'Turtle Neck' filter | ✗ Deviation | Step skipped in video |

## Deviations Detail

### Deviation 1: skipped

**Planned Action:** Select the 'Turtle Neck' filter in the Neck filter section
**Closest Match:** N/A
**Similarity Score:** 0.00
```

### Example Output

For the sample data in `data/` folder, the expected output would show:
- Steps that were successfully observed in the video
- Steps that had deviations (e.g., "Turtle Neck" filter not found)
- Cross-reference with test output assertions
- Timestamps for observed actions

## Architecture

The agent uses a multi-agent architecture with AutoGen:

1. **Log Parser Agent** - Extracts planned steps from JSON
2. **Video Analyzer Agent** - Processes video(s) and builds action timeline
3. **Test Output Parser Agent** - Parses test results
4. **Step Matcher Agent** - Matches planned steps with video evidence
5. **Deviation Analyzer Agent** - Analyzes deviations and cross-checks
6. **Report Generator Agent** - Generates final deviation report
7. **Orchestrator Agent** - Coordinates the workflow

## Configuration

### Groq API Configuration

The agent uses Groq API with the following configuration:
- **Model:** `openai/gpt-oss-120b`
- **Base URL:** `https://api.groq.com/openai/v1`
- **API Key:** Set in `GROQ_API_KEY` environment variable

Configuration is managed in `src/config/agent_config.py`.

### Environment Variables

Create a `.env` file with:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Project Structure

```
video-analysis-agent/
├── src/
│   ├── agents/          # AutoGen agents
│   ├── tools/           # Tool functions
│   ├── config/          # Configuration files
│   └── main.py          # Entry point
├── data/                # Sample input files
├── output/              # Generated reports
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **Video file not found:**
   - Ensure video path is correct
   - Check file permissions

2. **API key error:**
   - Verify `GROQ_API_KEY` is set in `.env`
   - Check API key is valid

3. **Import errors:**
   - Run `uv sync` to install dependencies
   - Ensure Python >= 3.13

4. **No matches found:**
   - Check video contains visible actions
   - Verify planning log has valid steps
   - Adjust similarity threshold if needed

## Development

### Running Tests

```bash
# Test individual components
uv run python -m src.tools.log_parser
uv run python -m src.tools.test_output_parser
```

### Adding New Features

1. Add tool functions in `src/tools/`
2. Create corresponding agents in `src/agents/`
3. Update `src/main.py` to integrate new features

## License

See LICENSE file for details.

## Contributing

This is an assessment project. For questions or issues, please refer to the assignment documentation.

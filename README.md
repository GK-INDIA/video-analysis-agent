# 🎬 Video Analysis Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![AutoGen](https://img.shields.io/badge/AutoGen-0.10.0-green.svg)
![Groq](https://img.shields.io/badge/Groq-API-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A multi-agent system that evaluates whether a Hercules test run was executed as planned by comparing planning logs, video evidence, and test outputs to detect deviations.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-how-to-run) • [Architecture](#-architecture) • [Documentation](#-documentation)

</div>

---

## 📋 Overview

The Video Analysis Agent is an intelligent system that validates test execution by analyzing three critical data sources:

<div align="center">

| 📝 Planning Log | 🎥 Video Evidence | 📊 Test Output |
|:---:|:---:|:---:|
| Intended actions | Actual execution | Final results |
| Step-by-step plan | Screen recordings | Assertions & outcomes |

</div>

The agent uses **semantic matching** and **multi-agent orchestration** to detect if claimed actions are visibly executed in videos and flags any deviations (skipped, altered, or not visible actions).

---

## ✨ Features

<div align="center">

| Feature | Description |
|:---:|:---|
| 🔍 **Log Parsing** | Extract planned steps from `agent_inner_logs.json` |
| 🎬 **Video Analysis** | Process single or multiple videos with frame extraction |
| 📄 **Test Output Parsing** | Parse XML/HTML test results |
| 🎯 **Semantic Matching** | Intelligent matching between planned and observed actions |
| 📈 **Deviation Detection** | Identify skipped, altered, or missing actions |
| 📝 **Report Generation** | Generate comprehensive Markdown/HTML reports |
| 🤖 **Multi-Agent Architecture** | AutoGen-powered agent orchestration |
| ⚡ **Groq API** | Powered by GPT-OSS-120B model |

</div>

---

## 🚀 Installation

### Prerequisites

- **Python** >= 3.13
- **[uv](https://github.com/astral-sh/uv)** package manager

### Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd video-analysis-agent

# 2. Install dependencies
uv sync

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your Groq API key

# 4. Run the agent
uv run python main.py
```

### Environment Setup

Create a `.env` file with your Groq API key:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

> 💡 **Note:** Get your API key from [Groq Console](https://console.groq.com/)

---

## 🎮 How to Run

### Basic Usage

Run with default input files:

```bash
uv run python main.py
```

### Advanced Usage

```bash
# Custom input files
uv run python main.py \
  --log data/agent_inner_logs.json \
  --video data/video.webm \
  --test-output data/test_result.xml \
  --output output/deviation_report.md

# Multiple videos
uv run python main.py \
  --video data/video1.webm data/video2.webm data/video3.webm

# HTML output
uv run python main.py --format html
```

### Command-Line Options

| Option | Description | Default |
|:---|:---|:---|
| `--log` | Path to `agent_inner_logs.json` | `data/agent_inner_logs.json` |
| `--video` | Path(s) to video file(s) | `data/video.webm` |
| `--test-output` | Path to test result file | `data/test_result.xml` |
| `--output` | Output path for report | `output/deviation_report.md` |
| `--format` | Output format (markdown/html) | `markdown` |

---

## 📁 Where Output is Saved

Reports are saved to the `output/` directory:

- **Default:** `output/deviation_report.md`
- **Custom:** Specify with `--output` flag
- **Formats:** Markdown (`.md`) or HTML (`.html`)

The output directory is created automatically if it doesn't exist.

---

## 🏗️ Architecture

### System Architecture Overview

```mermaid
graph TB
    subgraph Input["📥 Input Sources"]
        A[Planning Log<br/>agent_inner_logs.json]
        B[Video Evidence<br/>video.webm]
        C[Test Output<br/>test_result.xml/html]
    end
    
    subgraph Processing["⚙️ Processing Pipeline"]
        D[Log Parser Agent]
        E[Video Analyzer Agent]
        F[Test Output Agent]
        G[Step Matcher Agent]
        H[Deviation Analyzer Agent]
        I[Report Generator Agent]
    end
    
    subgraph Output["📤 Output"]
        J[Deviation Report<br/>Markdown/HTML]
    end
    
    A --> D
    B --> E
    C --> F
    
    D --> G
    E --> G
    F --> H
    
    G --> H
    H --> I
    I --> J
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style J fill:#f3e5f5
```

### Multi-Agent Workflow

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator as 🎯 Orchestrator Agent
    participant LogParser as 📝 Log Parser Agent
    participant VideoAnalyzer as 🎥 Video Analyzer Agent
    participant TestParser as 📊 Test Output Agent
    participant StepMatcher as 🎯 Step Matcher Agent
    participant DeviationAnalyzer as 🔍 Deviation Analyzer Agent
    participant ReportGen as 📄 Report Generator Agent
    
    User->>Orchestrator: Start Analysis
    Orchestrator->>LogParser: Parse Planning Log
    LogParser-->>Orchestrator: Planned Steps
    
    Orchestrator->>VideoAnalyzer: Analyze Video(s)
    VideoAnalyzer-->>Orchestrator: Action Timeline
    
    Orchestrator->>TestParser: Parse Test Output
    TestParser-->>Orchestrator: Test Results
    
    Orchestrator->>StepMatcher: Match Steps
    StepMatcher->>StepMatcher: Semantic Matching
    StepMatcher-->>Orchestrator: Match Results
    
    Orchestrator->>DeviationAnalyzer: Analyze Deviations
    DeviationAnalyzer->>DeviationAnalyzer: Cross-check
    DeviationAnalyzer-->>Orchestrator: Deviation Analysis
    
    Orchestrator->>ReportGen: Generate Report
    ReportGen-->>Orchestrator: Deviation Report
    Orchestrator-->>User: Complete Report
```

### Processing Steps Flow

```mermaid
flowchart LR
    subgraph Step1["Step 1: Parse Planning Log"]
        S1A[📄 JSON File]
        S1B[Extract Steps]
        S1C[Action Descriptions]
        S1A --> S1B --> S1C
    end
    
    subgraph Step2["Step 2: Inspect Video"]
        S2A[🎬 Video File]
        S2B[Extract Frames]
        S2C[Analyze Actions]
        S2D[Build Timeline]
        S2A --> S2B --> S2C --> S2D
    end
    
    subgraph Step3["Step 3: Cross-check Output"]
        S3A[📊 Test Results]
        S3B[Match Steps]
        S3C[Validate Consistency]
        S3D[Detect Deviations]
        S3A --> S3B --> S3C --> S3D
    end
    
    Step1 --> Step2
    Step2 --> Step3
    
    style Step1 fill:#e3f2fd
    style Step2 fill:#fff3e0
    style Step3 fill:#e8f5e9
```

### Agent Communication Pattern

```mermaid
graph TD
    O[🎯 Orchestrator Agent]
    
    O -->|Delegates| LP[📝 Log Parser Agent]
    O -->|Delegates| VA[🎥 Video Analyzer Agent]
    O -->|Delegates| TO[📊 Test Output Agent]
    
    LP -->|Planned Steps| SM[🎯 Step Matcher Agent]
    VA -->|Observed Actions| SM
    TO -->|Test Assertions| DA[🔍 Deviation Analyzer Agent]
    
    SM -->|Matches| DA
    DA -->|Findings| RG[📄 Report Generator Agent]
    RG -->|Report| O
    
    style O fill:#ffeb3b
    style LP fill:#2196f3
    style VA fill:#ff9800
    style TO fill:#4caf50
    style SM fill:#9c27b0
    style DA fill:#f44336
    style RG fill:#00bcd4
```

### Component Architecture

```mermaid
graph TB
    subgraph Agents["🤖 AutoGen Agents"]
        A1[Log Parser Agent]
        A2[Video Analyzer Agent]
        A3[Test Output Agent]
        A4[Step Matcher Agent]
        A5[Deviation Analyzer Agent]
        A6[Report Generator Agent]
        A7[Orchestrator Agent]
    end
    
    subgraph Tools["🛠️ Tools"]
        T1[log_parser.py]
        T2[video_analyzer.py]
        T3[action_detector.py]
        T4[test_output_parser.py]
        T5[step_matcher.py]
        T6[report_generator.py]
    end
    
    subgraph Config["⚙️ Configuration"]
        C1[agent_config.py<br/>Groq API Setup]
    end
    
    A1 --> T1
    A2 --> T2
    A2 --> T3
    A3 --> T4
    A4 --> T5
    A6 --> T6
    
    A1 --> C1
    A2 --> C1
    A3 --> C1
    A4 --> C1
    A5 --> C1
    A6 --> C1
    A7 --> C1
    
    style Agents fill:#e1f5ff
    style Tools fill:#fff4e1
    style Config fill:#e8f5e9
```

---

## 📊 Sample Inputs and Expected Outputs

### Input File Formats

#### 📝 Planning Log (`agent_inner_logs.json`)

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
      }
    }
  ]
}
```

**Key Fields:**
- `plan`: Full plan as numbered list
- `next_step`: Detailed step description
- `next_step_summary`: Brief step summary
- `is_assert`: Boolean indicating if this is an assertion

#### 🎬 Video File (`video.webm`)

- **Format:** WebM, MP4, or other formats supported by OpenCV
- **Content:** Screen recording of the test execution
- **Multiple videos:** Supported for full coverage

#### 📊 Test Output (`test_result.xml` or `test_result.html`)

**XML Format:**
```xml
<testsuite>
  <testcase>
    <failure message="EXPECTED RESULT: ... ACTUAL RESULT: ..."/>
    <properties>
      <property name="plan" value="1. Navigate..."/>
    </properties>
  </testcase>
</testsuite>
```

### 📈 Expected Output Format

The deviation report includes:

```markdown
# Deviation Report

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
```

---

## ⚙️ Configuration

### Groq API Configuration

The agent uses Groq API with the following settings:

| Setting | Value |
|:---|:---|
| **Model** | `openai/gpt-oss-120b` |
| **Base URL** | `https://api.groq.com/openai/v1` |
| **API Key** | Set in `GROQ_API_KEY` environment variable |

Configuration is managed in `src/config/agent_config.py`.

---

## 📂 Project Structure

```
video-analysis-agent/
├── 📁 src/
│   ├── 🤖 agents/              # AutoGen agents
│   │   ├── log_parser_agent.py
│   │   ├── video_analyzer_agent.py
│   │   ├── test_output_agent.py
│   │   ├── step_matcher_agent.py
│   │   ├── deviation_analyzer_agent.py
│   │   ├── report_generator_agent.py
│   │   └── orchestrator_agent.py
│   ├── 🛠️ tools/               # Tool functions
│   │   ├── log_parser.py
│   │   ├── video_analyzer.py
│   │   ├── action_detector.py
│   │   ├── test_output_parser.py
│   │   ├── step_matcher.py
│   │   └── report_generator.py
│   ├── ⚙️ config/              # Configuration
│   │   └── agent_config.py
│   └── 🚀 main.py              # Entry point
├── 📁 data/                    # Sample input files
├── 📁 output/                  # Generated reports
├── 📄 pyproject.toml           # Project dependencies
└── 📖 README.md               # This file
```

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|:---|:---|
| **Video file not found** | Ensure video path is correct and file has read permissions |
| **API key error** | Verify `GROQ_API_KEY` is set in `.env` file |
| **Import errors** | Run `uv sync` to install dependencies |
| **No matches found** | Check video contains visible actions, verify planning log has valid steps |

---

## 🧪 Development

### Running Tests

```bash
# Run comprehensive test suite
uv run python test_agent.py

# Test individual components
uv run python -m src.tools.log_parser
uv run python -m src.tools.test_output_parser
```

### Adding New Features

1. Add tool functions in `src/tools/`
2. Create corresponding agents in `src/agents/`
3. Update `src/main.py` to integrate new features

---

## 📚 Documentation

- **[BLOCKERS.md](BLOCKERS.md)** - Known issues and solutions
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Test execution results
- **[VIDEO_WALKTHROUGH_GUIDE.md](VIDEO_WALKTHROUGH_GUIDE.md)** - Guide for creating video walkthrough

---

## 📄 License

See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

This is an assessment project. For questions or issues, please refer to the assignment documentation.

---

<div align="center">

**Built with ❤️ using AutoGen and Groq API**

[⬆ Back to Top](#-video-analysis-agent)

</div>

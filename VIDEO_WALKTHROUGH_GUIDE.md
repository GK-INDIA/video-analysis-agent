# Video Walkthrough Guide

This guide provides a script and instructions for creating the video walkthrough screen recording for the Video Analysis Agent deliverable.

## Script Outline

### 1. Introduction (30 seconds)

**Content:**
- Brief overview of the Video Analysis Agent
- Purpose: Detect deviations between planned actions and video evidence
- What the agent does: Compares planning logs, video evidence, and test outputs

**Script:**
> "Welcome to the Video Analysis Agent demonstration. This agent evaluates whether a Hercules test run was executed as planned by comparing planning logs, video evidence, and test outputs to detect deviations. Let me show you how it works."

---

### 2. Explain Approach (2-3 minutes)

#### 2.1 Input Ingestion

**Content:**
- Show the three input files (planning log, video, test output)
- Explain how each is parsed
- Demonstrate file structure

**Script:**
> "The agent processes three types of inputs. First, the planning log - this JSON file contains the agent's intended step-by-step actions. Second, the video evidence - this captures the actual execution. And third, the test output - this provides the final test results and assertions. Let me show you the structure of each file..."

**Actions:**
- Open `data/agent_inner_logs.json` and highlight key fields (plan, next_step, next_step_summary)
- Show `data/video.webm` (brief preview)
- Open `data/test_result.xml` and highlight test outcome and properties

#### 2.2 Step Comparison

**Content:**
- Show how planned steps are extracted
- Demonstrate video frame extraction and analysis
- Explain action matching process
- Show how multiple videos are coordinated

**Script:**
> "The agent extracts planned steps from the log, then analyzes the video by extracting frames at regular intervals. Each frame is analyzed using vision API to detect UI elements, text content, and visible actions. The agent then uses semantic matching to compare planned actions with observed actions. If multiple videos are provided, timelines are merged for full coverage."

**Actions:**
- Show code snippet or explain the extraction process
- Demonstrate frame extraction (if possible)
- Explain semantic matching algorithm

#### 2.3 Report Generation

**Content:**
- Explain deviation detection logic
- Show how cross-checking with test output works
- Demonstrate report format

**Script:**
> "The agent matches each planned step with the video timeline. If a step is found with sufficient similarity, it's marked as observed. Otherwise, it's flagged as a deviation. The agent also cross-checks findings with the test output to validate consistency. Finally, a comprehensive deviation report is generated."

**Actions:**
- Explain deviation categories (observed, skipped, altered, not_visible)
- Show how test output assertions are used for validation

---

### 3. Live Run (3-4 minutes)

**Content:**
- Run the agent on sample Hercules artifacts from `data/` folder
- Show command execution
- Display processing steps in real-time
- Show agent interactions (if visible in console)

**Script:**
> "Now let's run the agent on the sample data. I'll execute the command and show you the processing steps in real-time."

**Actions:**
- Open terminal
- Run: `uv run python main.py`
- Show progress indicators
- Highlight each processing step:
  - "Step 1: Parsing Planning Log"
  - "Step 2: Analyzing Video(s)"
  - "Step 3: Parsing Test Output"
  - "Step 4: Matching Steps with Video Evidence"
  - "Step 5: Generating Deviation Report"
- Show summary statistics

**Command:**
```bash
uv run python main.py \
  --log data/agent_inner_logs.json \
  --video data/video.webm \
  --test-output data/test_result.xml \
  --output output/deviation_report.md
```

---

### 4. Display Final Report (1-2 minutes)

**Content:**
- Open the generated deviation report
- Walk through the report table
- Explain observed vs deviated actions
- Show timestamps and notes
- Highlight any deviations found

**Script:**
> "The analysis is complete. Let me show you the generated deviation report. Here you can see a summary with total steps, observed actions, and deviations. The detailed results table shows each planned step, whether it was observed in the video, and any notes including timestamps. Let me highlight the deviations that were found..."

**Actions:**
- Open `output/deviation_report.md` in editor/viewer
- Scroll through the report
- Point out:
  - Summary section
  - Detailed results table
  - Observed actions (☑)
  - Deviations (✗)
  - Timestamps for observed actions
  - Deviation details section
- Highlight specific deviations (e.g., "Turtle Neck filter not found")

---

### 5. Conclusion (30 seconds)

**Content:**
- Summary of capabilities
- Key features demonstrated

**Script:**
> "In summary, the Video Analysis Agent successfully processes planning logs, analyzes video evidence, and cross-checks with test outputs to detect deviations. It supports multiple videos, semantic matching, and generates comprehensive reports. Thank you for watching!"

**Actions:**
- Show final summary
- Highlight key features:
  - Multi-agent architecture
  - Semantic matching
  - Multiple video support
  - Comprehensive reporting

---

## Technical Requirements

### Screen Recording Software

- **Recommended:** OBS Studio, QuickTime (Mac), or similar
- **Resolution:** At least 1080p (1920x1080)
- **Frame Rate:** 30 FPS minimum
- **Audio:** Clear narration with minimal background noise

### Recording Settings

- **Screen Area:** Full screen or focused window
- **Audio:** System audio + microphone
- **Format:** MP4 or WebM
- **Quality:** High (for clarity of text and UI)

### Display Requirements

- **Terminal:** Use clear, readable font (e.g., Fira Code, Monaco, Consolas)
- **Font Size:** At least 12pt for terminal text
- **Color Scheme:** High contrast (dark background, light text recommended)
- **Window Size:** Terminal window should be large enough to show full output

---

## Files to Prepare

Before recording, ensure:

- [ ] Sample data ready in `data/` folder:
  - `agent_inner_logs.json`
  - `video.webm`
  - `test_result.xml` or `test_result.html`
- [ ] Agent configured and tested
- [ ] Example output report ready to display (`output/deviation_report.md`)
- [ ] Terminal with clear, readable font
- [ ] All dependencies installed (`uv sync` completed)
- [ ] Environment variables configured (`.env` file)

---

## Recording Checklist

### Pre-Recording

- [ ] Test run successful before recording
- [ ] All input files present and valid
- [ ] Output directory clean/ready
- [ ] API keys configured (Groq API key in `.env`)
- [ ] Terminal window sized appropriately
- [ ] Audio levels tested
- [ ] Screen resolution set to 1080p or higher
- [ ] Recording software configured and tested
- [ ] Script reviewed and practiced

### During Recording

- [ ] Speak clearly and at moderate pace
- [ ] Pause briefly between sections
- [ ] Highlight important UI elements
- [ ] Show full command execution
- [ ] Wait for processing to complete before moving on
- [ ] Explain what's happening at each step

### Post-Recording

- [ ] Review recording for clarity
- [ ] Check audio quality
- [ ] Verify all steps are visible
- [ ] Trim unnecessary pauses if needed
- [ ] Add captions/subtitles if required
- [ ] Export in required format
- [ ] Test playback on different devices

---

## Tips for Best Results

1. **Practice First:** Run through the entire script once before recording
2. **Clear Terminal:** Start with a clean terminal window
3. **Slow Down:** Don't rush - allow time for viewers to read text
4. **Zoom In:** Use zoom/zoom feature if text is too small
5. **Highlight:** Use cursor or highlighting to draw attention
6. **Pause:** Pause briefly after showing important information
7. **Error Handling:** If something goes wrong, explain and show recovery

---

## Estimated Duration

- **Total:** 7-10 minutes
- **Introduction:** 30 seconds
- **Explain Approach:** 2-3 minutes
- **Live Run:** 3-4 minutes
- **Display Report:** 1-2 minutes
- **Conclusion:** 30 seconds

---

## Example Command Sequence

```bash
# Show current directory
pwd

# List input files
ls -la data/

# Show planning log structure
cat data/agent_inner_logs.json | head -20

# Run the agent
uv run python main.py

# Show the generated report
cat output/deviation_report.md
```

---

## Notes

- Keep the video focused and concise
- Emphasize the three processing steps
- Show actual results, not just theory
- Make it clear how deviations are detected
- Highlight the multi-agent architecture if time permits

Good luck with your recording! 🎥


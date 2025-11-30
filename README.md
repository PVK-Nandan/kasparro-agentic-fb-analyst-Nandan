# Kasparro — Agentic Facebook Performance Analyst

An autonomous multi-agent system that diagnoses Facebook Ads performance, identifies ROAS fluctuation drivers, and recommends data-driven creative improvements.

## Quick Start

```bash
# Check Python version (requires >= 3.10)
python -V

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"  # Windows: set OPENAI_API_KEY=your-key-here

# Run the system
python src/run.py "Analyze ROAS drop in last 7 days"
```

## Data Setup

Place your Facebook Ads CSV file in one of two ways:

**Option 1: Full dataset**
```bash
export DATA_CSV=/path/to/synthetic_fb_ads_undergarments.csv
```

**Option 2: Use sample data**
```bash
# Copy sample data (included in repo)
cp data/sample_fb_ads.csv data/fb_ads.csv
# Edit config/config.yaml to set use_sample_data: true
```

See `data/README.md` for data format details.

## Configuration

Edit `config/config.yaml`:

```yaml
python: "3.10"
random_seed: 42
confidence_min: 0.6
use_sample_data: true
data_path: "data/sample_fb_ads.csv"
openai_model: "gpt-4"
max_insights: 5
```

## Repository Structure

```
├── src/
│   ├── run.py                      # Main CLI entry point
│   ├── orchestrator/
│   │   └── agent_orchestrator.py   # Agent coordination logic
│   ├── agents/
│   │   ├── planner.py              # Query decomposition
│   │   ├── data_agent.py           # Data loading & summarization
│   │   ├── insight_agent.py        # Hypothesis generation
│   │   ├── evaluator.py            # Quantitative validation
│   │   └── creative_generator.py   # Creative recommendations
│   └── utils/
│       └── helpers.py              # Shared utilities
├── prompts/                        # Structured prompt templates
├── reports/                        # Generated outputs
│   ├── report.md
│   ├── insights.json
│   └── creatives.json
├── logs/                          # Execution traces
├── tests/                         # Agent validation tests
└── config/                        # Configuration files
```

## Architecture

### Agent Flow Diagram

```
User Query
    ↓
┌─────────────────┐
│ Planner Agent   │ → Decomposes query into subtasks
└────────┬────────┘
         ↓
┌─────────────────┐
│ Data Agent      │ → Loads & summarizes dataset
└────────┬────────┘
         ↓
┌─────────────────┐
│ Insight Agent   │ → Generates hypotheses
└────────┬────────┘
         ↓
┌─────────────────┐
│ Evaluator Agent │ → Validates with quantitative analysis
└────────┬────────┘   (Feedback loop: retry low-confidence)
         ↓
┌─────────────────┐
│ Creative Gen    │ → Produces creative recommendations
└────────┬────────┘
         ↓
    Final Report
```

### Agent Responsibilities

1. **Planner**: Breaks user queries into structured subtasks (e.g., "identify ROAS drivers", "recommend creatives")
2. **Data Agent**: Loads CSV, computes key metrics, generates statistical summaries
3. **Insight Agent**: Forms hypotheses about performance patterns (audience fatigue, creative decay, etc.)
4. **Evaluator**: Validates hypotheses with quantitative checks, assigns confidence scores
5. **Creative Generator**: Produces new headlines/messages for low-CTR campaigns based on existing data

## Running Examples

```bash
# Analyze ROAS changes
python src/run.py "Why did ROAS drop in the last 7 days?"

# Find low-performing campaigns
python src/run.py "Which campaigns have CTR below 1.5%?"

# Get creative recommendations
python src/run.py "Suggest new creative messages for low-performing ads"

# Complex analysis
python src/run.py "Analyze performance by platform and recommend optimizations"
```

## Outputs

All outputs are generated in `reports/`:

- **report.md**: Human-readable markdown summary
- **insights.json**: Structured hypotheses with confidence scores
- **creatives.json**: Creative recommendations for low-CTR campaigns

## Validation & Testing

The system includes quantitative validation:

```bash
# Run evaluator tests
python -m pytest tests/test_evaluator.py

# Check logs for trace evidence
cat logs/execution_trace_*.json
```

## Observability

Execution traces are logged in `logs/` directory with:
- Agent inputs/outputs
- Confidence scores
- Validation results
- Timestamp information

## Key Design Decisions

### Prompt Architecture
- **Structured prompts** with explicit reasoning steps (Think → Analyze → Conclude)
- **JSON schemas** for consistent output parsing
- **Reflection loops** for low-confidence results

### Data Handling
- **Summarization over raw data**: Agents receive statistical summaries, not full CSVs
- **Missing data handling**: Graceful degradation when fields are null
- **Date-aware analysis**: Proper time-series grouping for trend detection

### Confidence Scoring
- Evaluator assigns 0-1 confidence to each hypothesis
- Hypotheses below threshold trigger re-analysis
- Final report includes only high-confidence insights

## Requirements

- Python 3.10+
- OpenAI API key
- Dependencies in `requirements.txt`

## Release Information

- **Version**: v1.0
- **Release Tag**: `v1.0`
- **Commit Hash**: [See GitHub release]

## Self-Review

See Pull Request: "self-review" for detailed design choices and architectural tradeoffs.

## Contact

For questions about this implementation:
- **Assignment**: Kasparro Applied AI Engineer
- **Repository**: kasparro-agentic-fb-analyst-nandan
- **Email**: grandmaster@kasparro.com
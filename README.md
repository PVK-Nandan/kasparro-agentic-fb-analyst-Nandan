# Kasparro — Agentic Facebook Performance Analyst

An autonomous multi-agent system that diagnoses Facebook Ads performance, identifies ROAS fluctuation drivers, and recommends data-driven creative improvements.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-00A67E?logo=openai&logoColor=white)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0-orange)](https://github.com/PVK-Nandan/kasparro-agentic-fb-analyst-nandan/releases/tag/v1.0)

## Quick Start

```bash
python -V  # should be >= 3.10
python -m venv .venv && source .venv/bin/activate  # win: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key-here"  # win: set OPENAI_API_KEY=your-key-here
python src/run.py "Analyze ROAS drop in last 7 days"
```

## Data

- Place the full CSV locally and set `DATA_CSV=/path/to/synthetic_fb_ads_undergarments.csv`
- Or copy a small sample to `data/sample_fb_ads.csv`
- See `data/README.md` for details

## Config

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

## Repo Map

```
kasparro-agentic-fb-analyst-nandan/
├── src/
│   ├── run.py                         # Main CLI entry point
│   ├── orchestrator/
│   │   └── agent_orchestrator.py      # Agent coordination logic
│   └── agents/
│       ├── planner.py                 # Query decomposition
│       ├── data_agent.py              # Data loading & summarization
│       ├── insight_agent.py           # Hypothesis generation
│       ├── evaluator.py               # Quantitative validation
│       └── creative_generator.py      # Creative recommendations
├── prompts/                           # *.md prompt files with variable placeholders
├── reports/                           # report.md, insights.json, creatives.json
├── logs/                              # JSON execution traces
├── tests/                             # test_evaluator.py
└── config/                            # config.yaml
```

## Run

```bash
make run  # or: python src/run.py "Analyze ROAS drop"
```

**Example queries:**
```bash
python src/run.py "Why did ROAS drop in the last 7 days?"
python src/run.py "Which campaigns have CTR below 1.5%?"
python src/run.py "Suggest new creative messages for low-performing ads"
python src/run.py "Analyze performance by platform and recommend optimizations"
```

## Outputs

- `reports/report.md` — Human-readable markdown summary
- `reports/insights.json` — Structured hypotheses with confidence scores
- `reports/creatives.json` — Creative recommendations for low-CTR campaigns

## Architecture

**Agent Flow:**
```
User Query → Planner → Data Agent → Insight Agent → Evaluator → Creative Generator → Final Report
```

**Agent Responsibilities:**
- **Planner**: Breaks user queries into structured subtasks
- **Data Agent**: Loads CSV, computes key metrics, generates statistical summaries
- **Insight Agent**: Forms hypotheses about performance patterns (audience fatigue, creative decay, etc.)
- **Evaluator**: Validates hypotheses with quantitative checks, assigns confidence scores
- **Creative Generator**: Produces new headlines/messages for low-CTR campaigns based on existing data

## Observability

- Execution traces logged in `logs/` directory with agent inputs/outputs, confidence scores, validation results, and timestamps
- Include Langfuse screenshots or JSON logs in `reports/observability/` (if applicable)

## Testing

```bash
# Run evaluator tests
python -m pytest tests/test_evaluator.py

# Check logs for trace evidence
cat logs/execution_trace_*.json
```

## Key Features

- **Structured prompts** with explicit reasoning steps (Think → Analyze → Conclude)
- **JSON schemas** for consistent output parsing
- **Reflection loops** for low-confidence results
- **Summarization over raw data**: Agents receive statistical summaries, not full CSVs
- **Confidence-based validation**: Hypotheses below threshold trigger re-analysis
- **Production-ready**: Logs, traceability, maintainability

## Release

- **Version**: v1.0
- **Release Tag**: [v1.0](https://github.com/PVK-Nandan/kasparro-agentic-fb-analyst-nandan/releases/tag/v1.0)
- **Status**: Stable

## Self-Review

- See [SELF_REVIEW.md](SELF_REVIEW.md) for detailed design choices and architectural tradeoffs
- Link to PR describing design choices & tradeoffs

## Requirements

- Python 3.10+
- OpenAI API key
- Dependencies in `requirements.txt`

## Contact

**Nandan Pakki V K**  
🧠 AI/ML Engineer | Autonomous Agent Systems Specialist

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nandan-pakki-v-k-01639b253/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PVK-Nandan)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:grandmaster@kasparro.com)

**Specializations:** Multi-Agent Systems • LangGraph • OpenAI • RAG Pipelines • Production ML

---

⭐ **If you found this project helpful, please consider giving it a star!**

Built with 💙 by [Nandan Pakki V K](https://github.com/PVK-Nandan)

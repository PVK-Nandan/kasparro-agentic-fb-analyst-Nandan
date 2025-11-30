# 🚀 Kasparro — Agentic Facebook Performance Analyst

An autonomous multi-agent system that diagnoses Facebook Ads performance, identifies ROAS fluctuation drivers, and recommends data-driven creative improvements.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-00A67E?logo=openai&logoColor=white)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-v1.0-orange)](https://github.com/PVK-Nandan/kasparro-agentic-fb-analyst-nandan/releases/tag/v1.0)

---

## ⚡ Quick Start

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

---

## 🔥 Features

| Capability | Description |
|------------|-------------|
| 📊 **Data Agent** | Ingests CSV → cleans → aggregates → summarizes metrics (ROAS, CTR, CPC, Spend) |
| 🧠 **Insight Agent** | Generates hypotheses from statistics & trends |
| ✔ **Evaluator Agent** | Validates claims, assigns confidence score (0-1), retries if weak |
| ✍ **Creative Generator** | Suggests new high-impact creatives based on winners/losers |
| 🔄 **Fully Orchestrated Pipeline** | Query → Planning → Data → Insights → Evaluation → Creatives |
| 🧾 **JSON + Markdown Output** | Reports saved with explanations, evidence, recommendations |
| 📜 **Logging + Observability** | Every run produces trace logs for debugging & audits |

---

## 📊 Data Setup

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

---

## ⚙️ Configuration

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

---

## 📂 Project Structure

```
kasparro-agentic-fb-analyst-nandan/
├── README.md                          📘 Main documentation + usage guide
├── requirements.txt                   📦 Dependency list (pinned)
├── Makefile                           ⚙️ Quick automation tasks
├── .gitignore                         🚫 Prevents sensitive/unnecessary files
├── agent_graph.md                     🧠 System architecture layout
├── SELF_REVIEW.md                     🔍 Deep design reasoning + decisions
├── SETUP_GUIDE.md                     🚀 Setup & execution instructions
├── SUBMISSION_SUMMARY.md              🏁 Final solution overview
│
├── config/
│   └── config.yaml                    🔧 All runtime configuration + model settings
│
├── src/
│   ├── run.py                         ▶ Entry point — run analysis here
│   ├── orchestrator/
│   │   └── agent_orchestrator.py      🤖 Multi-agent execution controller
│   ├── agents/
│   │   ├── planner.py                 🧭 Breaks query into subtasks
│   │   ├── data_agent.py              📊 CSV ingestion + metric summaries
│   │   ├── insight_agent.py           🧠 Hypothesis generation
│   │   ├── evaluator.py               🧾 Confidence-based validation
│   │   └── creative_generator.py      ✍ AI-powered creative suggestions
│   └── utils/
│       └── helpers.py                 🛠 Shared utilities + logging support
│
├── prompts/
│   ├── planner_prompt.md              🧩 Task planning instructions
│   ├── data_agent_prompt.md           🔢 Data summarization schema
│   ├── insight_agent_prompt.md        🔍 Insight reasoning framework
│   ├── evaluator_prompt.md            🧠 Confidence scoring + validation
│   └── creative_generator_prompt.md   🎨 Ad copy + creative direction
│
├── data/
│   ├── README.md                      📄 Data specification + schema
│   └── sample_fb_ads.csv              🧪 Example dataset for testing
│
├── tests/
│   └── test_evaluator.py              🧪 Unit tests for evaluator logic
│
├── reports/                           📤 Final analysis output (generated)
└── logs/                              📑 Trace logs for execution debugging
```

---

## 🏗️ Architecture

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

---

## 💻 Running Examples

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

---

## 📤 Outputs

All outputs are generated in `reports/`:

- **report.md**: Human-readable markdown summary
- **insights.json**: Structured hypotheses with confidence scores
- **creatives.json**: Creative recommendations for low-CTR campaigns

---

## 🧪 Validation & Testing

The system includes quantitative validation:

```bash
# Run evaluator tests
python -m pytest tests/test_evaluator.py

# Check logs for trace evidence
cat logs/execution_trace_*.json
```

---

## 📊 Observability

Execution traces are logged in `logs/` directory with:
- Agent inputs/outputs
- Confidence scores
- Validation results
- Timestamp information

---

## 🎯 Key Design Decisions

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

---

## 📋 Requirements

- Python 3.10+
- OpenAI API key
- Dependencies in `requirements.txt`

---

## 🎓 Why This Project Matters

This system demonstrates true applied AI engineering, not prompt hacking.

✔ Real software architecture  
✔ Confidence-based validation  
✔ Separate reasoning vs creativity modules  
✔ Scalable agent design  
✔ Logs, traceability, maintainability  

This is the type of pipeline you would use in production, not a hackathon demo.

---

## 📌 Release Information

- **Version**: v1.0
- **Release Tag**: `v1.0`
- **Status**: Stable

---

## 👨‍💻 About the Developer

**Nandan Pakki V K**

🧠 AI/ML Engineer | Autonomous Agent Systems Specialist

Building production-grade AI solutions with real-world impact

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nandan-pakki-v-k-01639b253/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PVK-Nandan)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:grandmaster@kasparro.com)

**💡 Specializations:**  
Multi-Agent Systems • LangGraph • OpenAI • RAG Pipelines • Production ML

**🔬 Currently Working On:**  
Autonomous AI agents for marketing analytics and business intelligence

---

⭐ **If you found this project helpful, please consider giving it a star!**

Built with 💙 by [Nandan Pakki V K](https://github.com/PVK-Nandan)

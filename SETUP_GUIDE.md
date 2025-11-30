# Setup Guide

## Prerequisites

- Python 3.10 or higher
- OpenAI API Key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd kasparro-agentic-fb-analyst-nandan
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   Set your OpenAI API key:
   ```bash
   # Windows
   set OPENAI_API_KEY=sk-your-key-here

   # Linux/Mac
   export OPENAI_API_KEY=sk-your-key-here
   ```

## Running the System

### Basic Usage
Run the analyst with a natural language query:

```bash
python src/run.py "Analyze why ROAS dropped last week"
```

### Using Custom Data
To analyze your own Facebook Ads data:

1. Ensure your CSV matches the format in `data/README.md`.
2. Run with the data path:

```bash
# Windows
set DATA_CSV=path/to/your_data.csv
python src/run.py "Analyze performance"

# Linux/Mac
DATA_CSV=path/to/your_data.csv python src/run.py "Analyze performance"
```

### Configuration
You can adjust system behavior in `config/config.yaml`:
- `confidence_min`: Minimum score to accept a hypothesis (default: 0.6)
- `max_insights`: Number of insights to generate
- `openai_model`: Model to use (default: gpt-4)

## Troubleshooting

**Issue: "OpenAI API key not found"**
- Ensure you set the environment variable `OPENAI_API_KEY`.

**Issue: "FileNotFoundError: data/sample_fb_ads.csv"**
- Ensure you are running the command from the root directory of the project.

**Issue: Low confidence insights**
- Try lowering `confidence_min` in `config.yaml` if the data is very noisy.

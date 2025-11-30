# Self Review & Design Decisions

## Architecture Choices

### 1. Multi-Agent Orchestration
I chose a sequential orchestration pattern with a feedback loop between the Insight and Evaluator agents. This ensures that:
- **Separation of Concerns**: Each agent has a specific role (Planning, Analysis, Validation, Creation).
- **Quality Control**: The Evaluator acts as a gatekeeper, preventing low-quality hallucinations from reaching the final report.
- **Refinement**: The feedback loop allows the system to "think harder" when initial hypotheses are weak.

### 2. Data Handling Strategy
Instead of passing the full dataframe to the LLM (which would exceed token limits and be expensive), I implemented a **Data Agent** that:
- Performs deterministic statistical analysis using Pandas.
- Generates a compressed JSON summary of key metrics, trends, and outliers.
- Passes this summary to the cognitive agents.
This hybrid approach combines the reliability of code-based calculation with the reasoning of LLMs.

### 3. Structured Outputs
All agents communicate via strictly typed JSON schemas. This prevents parsing errors and ensures that downstream agents receive predictable inputs. I used `json_mode` (implicit via prompt engineering) to guarantee valid JSON.

## Trade-offs

### Summarization vs. Granularity
**Decision**: Summarize data before sending to LLM.
**Trade-off**: The LLM cannot "see" every single row, so it might miss subtle micro-patterns.
**Mitigation**: The Data Agent's summary is comprehensive, covering multiple dimensions (Time, Campaign, Creative, Adset).

### Deterministic vs. Creative
**Decision**: Use Pandas for metrics, LLM for "why" and "what next".
**Reasoning**: LLMs are bad at math but good at reasoning. Python is great at math.
**Benefit**: 100% accurate calculations for ROAS, CTR changes, etc.

## Future Improvements

1. **Vector Memory**: Implement RAG to allow agents to recall past analyses.
2. **Tool Use**: Give the Data Agent the ability to write and execute its own Python code for ad-hoc queries.
3. **Visualizations**: Generate charts (matplotlib/seaborn) to include in the report.

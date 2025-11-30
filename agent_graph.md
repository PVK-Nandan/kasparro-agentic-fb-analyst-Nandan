# Agent Architecture

```mermaid
graph TD
    User([User Query]) --> Planner
    
    subgraph "Orchestration Layer"
        Planner[Planner Agent]
    end
    
    subgraph "Analysis Layer"
        DataAgent[Data Agent]
        InsightAgent[Insight Agent]
        Evaluator[Evaluator Agent]
    end
    
    subgraph "Creative Layer"
        CreativeGen[Creative Generator]
    end
    
    Planner -->|Execution Plan| DataAgent
    DataAgent -->|Data Summary| InsightAgent
    InsightAgent -->|Hypotheses| Evaluator
    
    Evaluator -->|Validated Insights| CreativeGen
    Evaluator -.->|Low Confidence (Retry)| InsightAgent
    
    CreativeGen -->|Recommendations| ReportGen[Report Generator]
    
    ReportGen -->|Final Report| Output([Markdown Report])
    ReportGen -->|JSON Data| OutputJSON([JSON Artifacts])
```

## Data Flow

1. **Planner**: Query -> Structured Plan
2. **Data Agent**: Plan + CSV -> Statistical Summary
3. **Insight Agent**: Summary -> Hypotheses
4. **Evaluator**: Hypotheses + Data -> Validated Insights + Confidence Scores
5. **Creative Generator**: Validated Insights + Low Performers -> Creative Recommendations

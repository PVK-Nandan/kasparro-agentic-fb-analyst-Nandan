"""
Agent Orchestrator - Coordinates the multi-agent workflow
"""

import json
from datetime import datetime
from pathlib import Path

from agents.planner import PlannerAgent
from agents.data_agent import DataAgent
from agents.insight_agent import InsightAgent
from agents.evaluator import EvaluatorAgent
from agents.creative_generator import CreativeGenerator


class AgentOrchestrator:
    """Orchestrates the execution of multiple agents in sequence"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.trace = []
        
        # Initialize agents
        self.planner = PlannerAgent(config, logger)
        self.data_agent = DataAgent(config, logger)
        self.insight_agent = InsightAgent(config, logger)
        self.evaluator = EvaluatorAgent(config, logger)
        self.creative_gen = CreativeGenerator(config, logger)
    
    def execute(self, query: str) -> dict:
        """Execute the full agent workflow"""
        
        self.logger.info("Starting agent orchestration", query=query)
        start_time = datetime.now()
        
        # Step 1: Planner decomposes query
        self.logger.info("Step 1: Planning")
        plan = self.planner.plan(query)
        self._log_step("planner", {"query": query}, plan)
        
        # Step 2: Data Agent loads and summarizes data
        self.logger.info("Step 2: Data loading and summarization")
        data_summary = self.data_agent.load_and_summarize()
        self._log_step("data_agent", {}, data_summary)
        
        # Step 3: Insight Agent generates hypotheses
        self.logger.info("Step 3: Hypothesis generation")
        hypotheses = self.insight_agent.generate_insights(
            query=query,
            plan=plan,
            data_summary=data_summary
        )
        self._log_step("insight_agent", {"plan": plan, "data_summary": data_summary}, hypotheses)
        
        # Step 4: Evaluator validates hypotheses
        self.logger.info("Step 4: Hypothesis validation")
        validated_insights = []
        retry_count = 0
        max_retries = self.config.get('max_retries', 2)
        
        for hypothesis in hypotheses:
            evaluation = self.evaluator.evaluate(
                hypothesis=hypothesis,
                data_summary=data_summary
            )
            
            # Retry logic for low confidence
            if evaluation['confidence'] < self.config['confidence_min'] and retry_count < max_retries:
                self.logger.info(
                    "Low confidence, retrying",
                    confidence=evaluation['confidence'],
                    hypothesis=hypothesis['hypothesis']
                )
                retry_count += 1
                # Re-generate this specific insight
                refined = self.insight_agent.refine_insight(
                    hypothesis=hypothesis,
                    evaluation=evaluation,
                    data_summary=data_summary
                )
                evaluation = self.evaluator.evaluate(refined, data_summary)
            
            if evaluation['confidence'] >= self.config['confidence_min']:
                validated_insights.append(evaluation)
        
        self._log_step("evaluator", {"hypotheses": hypotheses}, validated_insights)
        
        # Step 5: Creative Generator produces recommendations
        self.logger.info("Step 5: Creative generation")
        creatives = self.creative_gen.generate(
            insights=validated_insights,
            data_summary=data_summary
        )
        self._log_step("creative_generator", {"insights": validated_insights}, creatives)
        
        # Step 6: Generate final report
        self.logger.info("Step 6: Report generation")
        report = self._generate_report(
            query=query,
            insights=validated_insights,
            creatives=creatives
        )
        
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        self.logger.info(
            "Orchestration complete",
            execution_time=execution_time,
            insights_count=len(validated_insights),
            creatives_count=len(creatives)
        )
        
        return {
            'insights': validated_insights,
            'creatives': creatives,
            'report': report,
            'trace': self.trace,
            'execution_time': execution_time
        }
    
    def _log_step(self, agent: str, inputs: dict, outputs: dict):
        """Log agent execution step to trace"""
        self.trace.append({
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'inputs': inputs,
            'outputs': outputs
        })
    
    def _generate_report(self, query: str, insights: list, creatives: list) -> str:
        """Generate markdown report"""
        
        report = f"""# Facebook Ads Performance Analysis

**Query:** {query}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

Analysis completed with {len(insights)} validated insights and {len(creatives)} creative recommendations.

## Key Insights

"""
        
        for i, insight in enumerate(insights, 1):
            report += f"""
### {i}. {insight['hypothesis']}

**Confidence:** {insight['confidence']:.2%}

**Evidence:**
{insight['evidence']}

**Recommendation:**
{insight.get('recommendation', 'See creative recommendations below')}

---
"""
        
        if creatives:
            report += """
## Creative Recommendations

These recommendations are based on low-performing campaigns and existing high-performing creative patterns.

"""
            for i, creative in enumerate(creatives, 1):
                report += f"""
### Creative Set {i}

**Target Campaign:** {creative.get('campaign', 'N/A')}  
**Current CTR:** {creative.get('current_ctr', 'N/A')}  
**Issue:** {creative.get('issue', 'N/A')}

**Recommended Messages:**
"""
                for msg in creative.get('recommended_messages', []):
                    report += f"- {msg}\n"
                
                report += f"\n**Rationale:** {creative.get('rationale', 'N/A')}\n\n---\n"
        
        report += """
## Next Steps

1. Review high-confidence insights and prioritize action items
2. Test recommended creative variations with A/B testing
3. Monitor performance metrics after implementing changes
4. Re-run analysis in 7-14 days to measure impact

---

*Generated by Kasparro Agentic FB Analyst*
"""
        
        return report
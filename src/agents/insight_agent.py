class InsightAgent:
    def __init__(self):
        pass
"""
Insight Agent - Generates hypotheses about performance patterns
"""

import json
from pathlib import Path
from openai import OpenAI


class InsightAgent:
    """Generates data-driven hypotheses about ad performance"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.client = OpenAI()
        self.prompt_template = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """Load prompt template from file"""
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "insight_agent_prompt.md"
        with open(prompt_path, 'r') as f:
            return f.read()
    
    def generate_insights(self, query: str, plan: dict, data_summary: dict) -> list:
        """
        Generate hypotheses based on data patterns
        
        Returns list of hypotheses:
        [
            {
                "hypothesis": "...",
                "reasoning": "...",
                "data_evidence": "...",
                "category": "audience_fatigue" | "creative_decay" | "platform" | etc
            }
        ]
        """
        
        self.logger.info("Generating insights", query=query)
        
        # Prepare data summary for prompt
        summary_str = json.dumps(data_summary, indent=2, default=str)
        
        prompt = self.prompt_template.replace("{USER_QUERY}", query)
        prompt = prompt.replace("{PLAN}", json.dumps(plan, indent=2))
        prompt = prompt.replace("{DATA_SUMMARY}", summary_str)
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are an expert performance marketing analyst specializing in Facebook Ads optimization."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            result = json.loads(content)
            hypotheses = result.get('hypotheses', result) if isinstance(result, dict) else result
            
            # Limit to max_insights
            max_insights = self.config.get('max_insights', 5)
            hypotheses = hypotheses[:max_insights]
            
            self.logger.info("Insights generated", count=len(hypotheses))
            return hypotheses
            
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse insights", error=str(e))
            return []
    
    def refine_insight(self, hypothesis: dict, evaluation: dict, data_summary: dict) -> dict:
        """Refine a low-confidence hypothesis"""
        
        self.logger.info("Refining hypothesis", hypothesis=hypothesis.get('hypothesis', ''))
        
        refine_prompt = f"""
The following hypothesis had low confidence ({evaluation['confidence']:.2f}):

HYPOTHESIS: {hypothesis.get('hypothesis', '')}
REASONING: {hypothesis.get('reasoning', '')}

EVALUATOR FEEDBACK:
{evaluation.get('reasoning', '')}

DATA SUMMARY:
{json.dumps(data_summary, indent=2, default=str)}

Please refine this hypothesis to be more specific and quantitatively grounded.

Return JSON format:
{{
    "hypothesis": "refined hypothesis statement",
    "reasoning": "step-by-step analysis",
    "data_evidence": "specific metrics",
    "category": "audience_fatigue|creative_decay|platform|budget|targeting|other"
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are an expert analyst refining performance hypotheses."},
                {"role": "user", "content": refine_prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            refined = json.loads(content)
            self.logger.info("Hypothesis refined")
            return refined
            
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse refined hypothesis", error=str(e))
            return hypothesis  # Return original if refinement fails
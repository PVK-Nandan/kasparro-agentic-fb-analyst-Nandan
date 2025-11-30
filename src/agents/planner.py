"""
Planner Agent - Decomposes user queries into structured subtasks
"""

import json
from pathlib import Path
from openai import OpenAI


class PlannerAgent:
    """Breaks down user queries into actionable subtasks"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.client = OpenAI()
        self.prompt_template = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """Load prompt template from file"""
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "planner_prompt.md"
        with open(prompt_path, 'r') as f:
            return f.read()
    
    def plan(self, query: str) -> dict:
        """
        Decompose query into structured plan
        
        Returns:
            {
                "subtasks": [...],
                "analysis_type": "roas_analysis" | "ctr_analysis" | "creative_audit",
                "requires_creative": bool
            }
        """
        
        self.logger.info("Planner analyzing query", query=query)
        
        prompt = self.prompt_template.replace("{USER_QUERY}", query)
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are an expert marketing analyst planning a Facebook Ads performance analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            plan = json.loads(content)
            self.logger.info("Plan generated", subtask_count=len(plan.get('subtasks', [])))
            return plan
            
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse planner response", error=str(e))
            # Fallback plan
            return {
                "subtasks": [
                    "Load and analyze Facebook Ads data",
                    "Identify performance patterns",
                    "Generate insights",
                    "Provide recommendations"
                ],
                "analysis_type": "general",
                "requires_creative": True
            }
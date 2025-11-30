"""
Evaluator Agent - Validates hypotheses with quantitative analysis
"""

import json
from pathlib import Path
from openai import OpenAI


class EvaluatorAgent:
    """Validates hypotheses and assigns confidence scores"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.client = OpenAI()
        self.prompt_template = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """Load prompt template from file"""
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "evaluator_prompt.md"
        with open(prompt_path, 'r') as f:
            return f.read()
    
    def evaluate(self, hypothesis: dict, data_summary: dict) -> dict:
        """
        Validate hypothesis with quantitative checks
        
        Returns:
        {
            "hypothesis": "...",
            "confidence": 0.85,
            "evidence": "...",
            "reasoning": "...",
            "recommendation": "...",
            "metrics": {...}
        }
        """
        
        self.logger.info("Evaluating hypothesis", hypothesis=hypothesis.get('hypothesis', ''))
        
        # Prepare prompt
        summary_str = json.dumps(data_summary, indent=2, default=str)
        hypothesis_str = json.dumps(hypothesis, indent=2)
        
        prompt = self.prompt_template.replace("{HYPOTHESIS}", hypothesis_str)
        prompt = prompt.replace("{DATA_SUMMARY}", summary_str)
        prompt = prompt.replace("{CONFIDENCE_MIN}", str(self.config['confidence_min']))
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are a quantitative analyst validating marketing hypotheses with rigorous statistical reasoning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for consistency
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            evaluation = json.loads(content)
            
            confidence = evaluation.get('confidence', 0.5)
            self.logger.info(
                "Evaluation complete",
                confidence=confidence,
                passed=confidence >= self.config['confidence_min']
            )
            
            return evaluation
            
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse evaluation", error=str(e))
            # Return low-confidence fallback
            return {
                "hypothesis": hypothesis.get('hypothesis', ''),
                "confidence": 0.3,
                "evidence": "Unable to validate",
                "reasoning": "Evaluation parsing failed",
                "recommendation": "Manual review required"
            }
    
    def batch_evaluate(self, hypotheses: list, data_summary: dict) -> list:
        """Evaluate multiple hypotheses"""
        results = []
        for hypothesis in hypotheses:
            evaluation = self.evaluate(hypothesis, data_summary)
            results.append(evaluation)
        return results
"""
Creative Generator - Produces new creative recommendations for low-CTR campaigns
"""

import json
from pathlib import Path
from openai import OpenAI


class CreativeGenerator:
    """Generates creative message recommendations based on data patterns"""
    
    def __init__(self, config: dict, logger):
        self.config = config
        self.logger = logger
        self.client = OpenAI()
        self.prompt_template = self._load_prompt()
    
    def _load_prompt(self) -> str:
        """Load prompt template from file"""
        prompt_path = Path(__file__).parent.parent.parent / "prompts" / "creative_generator_prompt.md"
        with open(prompt_path, 'r') as f:
            return f.read()
    
    def generate(self, insights: list, data_summary: dict) -> list:
        """
        Generate creative recommendations for low-performing campaigns
        
        Returns list of creative recommendations:
        [
            {
                "campaign": "...",
                "current_ctr": 0.012,
                "issue": "...",
                "recommended_messages": [...],
                "rationale": "...",
                "inspired_by": "..."
            }
        ]
        """
        
        self.logger.info("Generating creative recommendations")
        
        # Extract low performers from data
        low_performers = data_summary.get('low_performers', [])
        top_messages = data_summary.get('creative_performance', {}).get('top_messages', [])
        
        if not low_performers:
            self.logger.info("No low performers found, skipping creative generation")
            return []
        
        # Prepare prompt
        insights_str = json.dumps(insights, indent=2, default=str)
        low_performers_str = json.dumps(low_performers, indent=2, default=str)
        top_messages_str = json.dumps(top_messages, indent=2, default=str)
        
        prompt = self.prompt_template.replace("{INSIGHTS}", insights_str)
        prompt = prompt.replace("{LOW_PERFORMERS}", low_performers_str)
        prompt = prompt.replace("{TOP_MESSAGES}", top_messages_str)
        prompt = prompt.replace("{LOW_CTR_THRESHOLD}", str(self.config['low_ctr_threshold']))
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are a creative strategist specializing in direct-response ad copy for e-commerce brands."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,  # Higher temperature for creative diversity
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
            creatives = result.get('recommendations', result) if isinstance(result, dict) else result
            
            self.logger.info("Creative recommendations generated", count=len(creatives))
            return creatives
            
        except json.JSONDecodeError as e:
            self.logger.error("Failed to parse creative recommendations", error=str(e))
            return []
    
    def generate_for_campaign(self, campaign: str, current_message: str, 
                             issue: str, top_patterns: list) -> list:
        """Generate specific messages for a single campaign"""
        
        prompt = f"""
Generate 5 new creative messages for this underperforming campaign:

CAMPAIGN: {campaign}
CURRENT MESSAGE: {current_message}
ISSUE: {issue}

HIGH-PERFORMING PATTERNS:
{json.dumps(top_patterns, indent=2)}

Requirements:
- Messages should be concise (under 100 characters)
- Focus on benefits, urgency, or social proof
- Maintain brand voice
- Test different angles (features, benefits, scarcity, social proof)

Return JSON array of 5 message strings.
"""
        
        response = self.client.chat.completions.create(
            model=self.config['openai_model'],
            messages=[
                {"role": "system", "content": "You are a direct-response copywriter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            messages = json.loads(content)
            return messages if isinstance(messages, list) else []
            
        except json.JSONDecodeError:
            return []
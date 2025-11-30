#!/usr/bin/env python3
"""
Kasparro Agentic Facebook Performance Analyst
Main entry point for the multi-agent system
"""

import os
import sys
import json
import yaml
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from orchestrator.agent_orchestrator import AgentOrchestrator
from utils.helpers import setup_logging, save_json, save_markdown


def load_config():
    """Load configuration from config.yaml"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Override data path from environment if set
    if os.getenv('DATA_CSV'):
        config['data_path'] = os.getenv('DATA_CSV')
        config['use_sample_data'] = False
    
    return config


def main(query: str):
    """Main execution function"""
    
    # Load configuration
    config = load_config()
    
    # Setup logging
    logger = setup_logging(config)
    logger.info("Starting Kasparro Agentic FB Analyst", query=query)
    
    # Validate OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY environment variable not set")
        print("❌ Error: Please set OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    # Create output directories
    output_dir = Path(config['output_dir'])
    output_dir.mkdir(exist_ok=True)
    log_dir = Path(config['log_dir'])
    log_dir.mkdir(exist_ok=True)
    
    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator(config, logger)
        
        # Execute agent workflow
        logger.info("Executing agent workflow")
        result = orchestrator.execute(query)
        
        # Save outputs
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save insights.json
        insights_path = output_dir / "insights.json"
        save_json(result['insights'], insights_path)
        logger.info(f"Saved insights to {insights_path}")
        
        # Save creatives.json
        creatives_path = output_dir / "creatives.json"
        save_json(result['creatives'], creatives_path)
        logger.info(f"Saved creatives to {creatives_path}")
        
        # Save report.md
        report_path = output_dir / "report.md"
        save_markdown(result['report'], report_path)
        logger.info(f"Saved report to {report_path}")
        
        # Save execution trace
        trace_path = log_dir / f"execution_trace_{timestamp}.json"
        save_json(result['trace'], trace_path)
        logger.info(f"Saved execution trace to {trace_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ Analysis Complete!")
        print("="*60)
        print(f"\n📊 Generated {len(result['insights'])} insights")
        print(f"💡 Generated {len(result['creatives'])} creative recommendations")
        print(f"\n📁 Outputs saved to:")
        print(f"   - {insights_path}")
        print(f"   - {creatives_path}")
        print(f"   - {report_path}")
        print(f"\n📝 View the full report:")
        print(f"   cat {report_path}")
        print("\n" + "="*60)
        
    except Exception as e:
        logger.error("Execution failed", error=str(e), exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/run.py 'Your query here'")
        print("\nExample queries:")
        print('  python src/run.py "Analyze ROAS drop in last 7 days"')
        print('  python src/run.py "Which campaigns have low CTR?"')
        print('  python src/run.py "Recommend new creative messages"')
        sys.exit(1)
    
    query = sys.argv[1]
    main(query)
import json
import logging
import sys
from pathlib import Path
import structlog

def setup_logging(config: dict):
    """Configure structured logging"""
    log_dir = Path(config.get('log_dir', 'logs'))
    log_dir.mkdir(exist_ok=True)
    
    # Simple configuration for structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()

def save_json(data: dict | list, path: Path):
    """Save data to JSON file"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

def save_markdown(content: str, path: Path):
    """Save content to Markdown file"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
"""Configuration parsing and validation."""
import json
import logging
from pathlib import Path
from typing import Dict, Any
from jsonschema import validate, ValidationError
from pydantic import BaseModel, field_validator

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "slide_number": {"type": "integer", "minimum": 1},
        "replacements": {"type": "object"}
    },
    "required": ["slide_number", "replacements"],
    "additionalProperties": False
}

class ReportConfig(BaseModel):
    slide_number: int
    replacements: Dict[str, Any]
    
    @field_validator('slide_number')
    @classmethod
    def validate_slide_number(cls, v):
        if v < 1:
            raise ValueError('slide_number must be >= 1')
        return v

def load_config(config_path: Path) -> ReportConfig:
    """Load and validate configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        validate(data, CONFIG_SCHEMA)
        config = ReportConfig(**data)
        logger.info(f"Loaded config for slide {config.slide_number}")
        return config
        
    except (json.JSONDecodeError, ValidationError, ValueError) as e:
        logger.error(f"Config validation failed: {e}")
        raise
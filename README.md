# PPT Report Generator

Secure PowerPoint report generator that replaces placeholders in slides based on JSON configuration.

## Features

- JSON schema validation for configuration
- Secure file operations with path sanitization
- Atomic file writes
- Structured logging
- CLI interface
- Unit tests

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.report_generator.cli \
  --config report_config.json \
  --input input_PPT/SMBC.pptx \
  --output-dir output
```

## Configuration

Example `report_config.json`:

```json
{
  "slide_number": 2,
  "replacements": {
    "MPE": "$120 B",
    "decrease_percent": "3.5%",
    "date": "August 2025"
  }
}
```

## Testing

```bash
pytest tests/
```

## Docker

```bash
docker build -t ppt-generator .
docker run -v $(pwd):/app ppt-generator python -m src.report_generator.cli --help
```

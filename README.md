# PPT Report Generator

Secure PowerPoint report generator that replaces placeholders in slides based on JSON configuration.

## Features

- JSON schema validation for configuration
- Secure file operations with path sanitization
- Atomic file writes
- Structured logging
- CLI interface
- Unit tests

## Installation & Usage

### Option 1: Native Python

**Install:**
```bash
pip install -r requirements.txt
```

**Run:**
```bash
python -m src.report_generator.cli \
  --config report_config.json \
  --input input_PPT/SMBC.pptx \
  --output-dir output
```

### Option 2: Docker

**Build:**
```bash
docker build -t ppt-generator .
```

**Run:**
```bash
docker run -v $(pwd):/app ppt-generator \
  python -m src.report_generator.cli \
  --config report_config.json \
  --input input_PPT/SMBC.pptx \
  --output-dir output
```

## Configuration

Example `report_config.json` with all slide 2 placeholders:

```json
{
  "slide_number": 2,
  "replacements": {
    "MM/DD/YYYY": "08/27/2025",
    "XXX": "120",
    "Y%": "3.5%",
    "YYY": "135",
    "XX%": "12%",
    "YY%": "75%",
    "XXM": "200",
    "YYK": "450",
    "XX K": "50",
    "YYM": "120",
    "XXK": "20",
    "XX B": "45",
    "XXB": "32",
    "YYB": "50"
  }
}
```

## Testing

```bash
pytest tests/
```

## Web Interface

### Quick Start
**Backend (Terminal 1):**
```bash
cd web
pip install -r backend/requirements.txt
python start_backend.py
```

**Frontend (Terminal 2):**
```bash
cd web/frontend
npm install
npm start
```

Open http://localhost:3000

### Features
- Visual slide preview
- Real-time placeholder editing
- One-click report generation
- Modern responsive UI

## Output

Generates timestamped reports:
```
output/report_generated_YYYYMMDD_HHMMSS.pptx
```

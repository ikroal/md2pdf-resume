# md2pdf-resume

Generate PDF resumes from Markdown.

## Install

```bash
pip install -e .
playwright install chromium
```

## Usage

```bash
# Initialize templates (Chinese)
md2pdf-resume init

# Initialize templates (English)
md2pdf-resume init --lang en

# Edit resume.md and resume.css, then generate
md2pdf-resume generate

# Custom paths
md2pdf-resume generate --md my_resume.md --css style.css --output my_resume.pdf

# Use built-in template
md2pdf-resume generate --md resume.md --template default
```

## Development

```bash
pip install -e ".[dev]"
pytest -m "not integration"
ruff format src/ tests/
ruff check src/ tests/
mypy src/
```

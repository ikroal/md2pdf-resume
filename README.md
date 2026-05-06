# md2pdf-resume

[![CI](https://github.com/ikroal/md2pdf-resume/actions/workflows/ci.yml/badge.svg)](https://github.com/ikroal/md2pdf-resume/actions/workflows/ci.yml)

Generate PDF resumes from Markdown.

## Install

```bash
uv pip install -e .
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

# Custom CSS file
md2pdf-resume generate --md my_resume.md --css style.css --output my_resume.pdf

# Use built-in style
md2pdf-resume generate --md resume.md --css default
```

## Development

```bash
uv sync --dev
uv run pytest tests/ -v -m "not integration"
uv run ruff format src/ tests/
uv run ruff check src/ tests/
uv run mypy src/
```

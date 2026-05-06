"""Configuration and default values."""

from pathlib import Path

TEMPLATES_DIR: Path = Path(__file__).parent / "templates"

DEFAULTS: dict[str, str | None] = {
    "md": "resume.md",
    "css": "resume.css",
    "output": None,
    "lang": "zh",
}


def get_template_path(name: str) -> Path | None:
    """Return path to a built-in CSS template, or None if not found."""
    css_path = TEMPLATES_DIR / f"{name}.css"
    return css_path if css_path.is_file() else None


def get_template_md_path(lang: str) -> Path | None:
    """Return path to a built-in MD template for the given language."""
    if lang == "zh":
        md_path = TEMPLATES_DIR / "default.md"
    elif lang == "en":
        md_path = TEMPLATES_DIR / "default_en.md"
    else:
        return None
    return md_path if md_path.is_file() else None

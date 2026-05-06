from pathlib import Path

from md2pdf_resume.config import DEFAULTS, TEMPLATES_DIR, get_template_md_path, get_template_path


def test_templates_dir_exists() -> None:
    assert TEMPLATES_DIR.is_dir()


def test_templates_dir_contains_default_md() -> None:
    assert (TEMPLATES_DIR / "default.md").is_file()


def test_templates_dir_contains_default_en_md() -> None:
    assert (TEMPLATES_DIR / "default_en.md").is_file()


def test_templates_dir_contains_default_css() -> None:
    assert (TEMPLATES_DIR / "default.css").is_file()


def test_defaults_has_required_keys() -> None:
    assert "md" in DEFAULTS
    assert "css" in DEFAULTS
    assert "output" in DEFAULTS
    assert "lang" in DEFAULTS


def test_get_template_path_default() -> None:
    path = get_template_path("default")
    assert path == TEMPLATES_DIR / "default.css"


def test_get_template_path_unknown_returns_none() -> None:
    path = get_template_path("nonexistent")
    assert path is None


def test_get_template_md_path_zh() -> None:
    path = get_template_md_path("zh")
    assert path == TEMPLATES_DIR / "default.md"


def test_get_template_md_path_en() -> None:
    path = get_template_md_path("en")
    assert path == TEMPLATES_DIR / "default_en.md"


def test_get_template_md_path_unknown_returns_none() -> None:
    path = get_template_md_path("xx")
    assert path is None

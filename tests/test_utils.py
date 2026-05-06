from pathlib import Path

import pytest

from md2pdf_resume.utils import check_playwright_browser, copy_template_file


def test_copy_template_file_creates_file(tmp_path: Path) -> None:
    src = tmp_path / "src.txt"
    src.write_text("hello")
    dst = tmp_path / "dst.txt"

    copy_template_file(src, dst)

    assert dst.exists()
    assert dst.read_text() == "hello"


def test_copy_template_file_raises_on_missing_src(tmp_path: Path) -> None:
    src = tmp_path / "missing.txt"
    dst = tmp_path / "dst.txt"

    with pytest.raises(FileNotFoundError):
        copy_template_file(src, dst)


def test_copy_template_file_raises_on_existing_dst(tmp_path: Path) -> None:
    src = tmp_path / "src.txt"
    src.write_text("hello")
    dst = tmp_path / "dst.txt"
    dst.write_text("existing")

    with pytest.raises(FileExistsError):
        copy_template_file(src, dst)

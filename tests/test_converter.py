from pathlib import Path

import pytest
from pypdf import PdfReader

from md2pdf_resume.converter import convert


@pytest.mark.integration
def test_convert_creates_pdf(tmp_path: Path) -> None:
    md_file = tmp_path / "test.md"
    md_file.write_text("# Hello World\n\nThis is a test.")
    css_file = tmp_path / "test.css"
    css_file.write_text("body { font-size: 12px; }")
    output = tmp_path / "out.pdf"

    convert(md_file, css_file, output)

    assert output.exists()
    reader = PdfReader(str(output))
    assert len(reader.pages) >= 1


@pytest.mark.integration
def test_convert_single_page(tmp_path: Path) -> None:
    md_file = tmp_path / "test.md"
    md_file.write_text("# Short\n\nJust a line.")
    css_file = tmp_path / "test.css"
    css_file.write_text("body { font-size: 12px; }")
    output = tmp_path / "out.pdf"

    convert(md_file, css_file, output)

    reader = PdfReader(str(output))
    assert len(reader.pages) == 1

from md2pdf_resume.html_builder import build_html


def test_build_html_returns_valid_structure() -> None:
    md = "# Hello"
    css = "body { color: red; }"
    result = build_html(md, css)

    assert "<!doctype html>" in result
    assert "<html" in result
    assert "</html>" in result


def test_build_html_includes_css() -> None:
    md = "# Hello"
    css = "body { color: red; }"
    result = build_html(md, css)

    assert "body { color: red; }" in result


def test_build_html_converts_markdown_heading() -> None:
    md = "# Hello World"
    css = ""
    result = build_html(md, css)

    assert "<h1>" in result
    assert "Hello World" in result


def test_build_html_converts_markdown_list() -> None:
    md = "- item 1\n- item 2"
    css = ""
    result = build_html(md, css)

    assert "<ul>" in result
    assert "<li>" in result


def test_build_html_has_write_container() -> None:
    md = "# Test"
    css = ""
    result = build_html(md, css)

    assert 'id="write"' in result


def test_build_html_lang_zh() -> None:
    md = "# Test"
    css = ""
    result = build_html(md, css)

    assert 'lang="zh-CN"' in result

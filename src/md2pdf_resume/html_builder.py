"""Build complete HTML documents from Markdown and CSS."""

import markdown


def build_html(markdown_text: str, css_text: str) -> str:
    """Convert Markdown text to a complete HTML document with embedded CSS."""
    body_html = markdown.markdown(markdown_text, extensions=["extra", "sane_lists"])
    return _wrap_html(body_html, css_text)


def _wrap_html(body_html: str, css_text: str) -> str:
    """Wrap HTML body with DOCTYPE, head (CSS), and container div."""
    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n'
        "  <head>\n"
        '    <meta charset="utf-8" />\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        "    <style>\n"
        f"{css_text}\n"
        "    </style>\n"
        "  </head>\n"
        "  <body>\n"
        f'    <div id="write">{body_html}</div>\n'
        "  </body>\n"
        "</html>\n"
    )

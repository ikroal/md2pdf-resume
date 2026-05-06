import asyncio
import re
from pathlib import Path
from typing import cast

import markdown
from pypdf import PdfReader
from playwright.async_api import async_playwright


ROOT = Path(__file__).resolve().parent
MD_FILE = ROOT / "resume_template.md"
CSS_FILE = ROOT / "resume.css"
OUT_PDF = ROOT / "杨溢-数据库内核研发.pdf"


def strip_line_prefixes(text: str) -> str:
    cleaned: list[str] = []
    for line in text.splitlines():
        cleaned.append(re.sub(r"^#[A-Za-z0-9]{2}\|", "", line))
    return "\n".join(cleaned)


def build_html(markdown_text: str, css_text: str) -> str:
    body_html = markdown.markdown(markdown_text, extensions=["extra", "sane_lists"])
    return f"""<!doctype html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
<style>
{css_text}
    </style>
  </head>
  <body>
    <div id=\"write\">{body_html}</div>
  </body>
</html>
"""


async def measure_scale(markdown_text: str, css_text: str) -> float:
    html = build_html(markdown_text, css_text)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.set_content(html, wait_until="networkidle")
        await page.emulate_media(media="print")

        content_height = cast(
            float,
            await page.evaluate(
            """
            () => {
              const write = document.querySelector('#write');
              return write ? write.getBoundingClientRect().height : 0;
            }
            """
            ),
        )
        await browser.close()

    available_height = 1123 - (10 / 25.4) * 96 * 2
    if content_height <= 0:
        return 1.0
    ratio = available_height / content_height
    return min(1.0, max(0.72, ratio))


async def generate_pdf(markdown_text: str, css_text: str, output: Path, scale: float) -> None:
    html = build_html(markdown_text, css_text)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 794, "height": 1123})
        await page.set_content(html, wait_until="networkidle")
        await page.emulate_media(media="print")
        _ = await page.pdf(
            path=str(output),
            format="A4",
            scale=scale,
            print_background=True,
            prefer_css_page_size=True,
        )
        await browser.close()


async def main() -> None:
    md_text = strip_line_prefixes(MD_FILE.read_text(encoding="utf-8"))
    css_text = strip_line_prefixes(CSS_FILE.read_text(encoding="utf-8"))

    scale = await measure_scale(md_text, css_text)
    await generate_pdf(md_text, css_text, OUT_PDF, scale)

    pages = len(PdfReader(str(OUT_PDF)).pages)
    min_scale = 0.55
    step = 0.03
    while pages > 1 and scale > min_scale:
        scale = round(max(min_scale, scale - step), 3)
        await generate_pdf(md_text, css_text, OUT_PDF, scale)
        pages = len(PdfReader(str(OUT_PDF)).pages)

    print(f"Generated: {OUT_PDF}")
    print(f"Scale: {scale}")
    print(f"Pages: {pages}")


if __name__ == "__main__":
    asyncio.run(main())

"""Convert Markdown to PDF via HTML and Playwright."""

import asyncio
from pathlib import Path
from typing import cast

from pypdf import PdfReader

from md2pdf_resume.html_builder import build_html

MIN_SCALE = 0.55
MAX_SCALE = 1.0
DEFAULT_SCALE = 0.72
SCALE_STEP = 0.03
PAGE_WIDTH = 794
PAGE_HEIGHT = 1123
MARGIN_MM = 10


def convert(md_path: Path, css_path: Path, output: Path) -> None:
    """Read MD and CSS files, generate a single-page PDF."""
    md_text = md_path.read_text(encoding="utf-8")
    css_text = css_path.read_text(encoding="utf-8")
    html = build_html(md_text, css_text)
    _run_async_convert(html, output)


def _run_async_convert(html: str, output: Path) -> None:
    """Run the async PDF generation pipeline."""
    asyncio.run(_async_convert(html, output))


async def _async_convert(html: str, output: Path) -> None:
    """Measure scale and generate PDF, shrinking until single page."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        scale = await _measure_scale(browser, html)
        await _generate_pdf(browser, html, output, scale)

        pages = _count_pages(output)
        while pages > 1 and scale > MIN_SCALE:
            scale = round(max(MIN_SCALE, scale - SCALE_STEP), 3)
            await _generate_pdf(browser, html, output, scale)
            pages = _count_pages(output)

        await browser.close()

    print(f"Generated: {output}")
    print(f"Scale: {scale}")
    print(f"Pages: {pages}")


async def _measure_scale(browser: object, html: str) -> float:
    """Measure content height and calculate scale to fit one page."""
    from playwright.async_api import Browser

    browser = cast(Browser, browser)
    page = await browser.new_page(viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT})
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
    await page.close()

    available_height = PAGE_HEIGHT - (MARGIN_MM / 25.4) * 96 * 2
    if content_height <= 0:
        return MAX_SCALE
    ratio = available_height / content_height
    return min(MAX_SCALE, max(DEFAULT_SCALE, ratio))


async def _generate_pdf(
    browser: object, html: str, output: Path, scale: float
) -> None:
    """Render HTML to PDF at the given scale."""
    from playwright.async_api import Browser

    browser = cast(Browser, browser)
    page = await browser.new_page(viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT})
    await page.set_content(html, wait_until="networkidle")
    await page.emulate_media(media="print")
    await page.pdf(
        path=str(output),
        format="A4",
        scale=scale,
        print_background=True,
        prefer_css_page_size=True,
    )
    await page.close()


def _count_pages(pdf_path: Path) -> int:
    """Count pages in a PDF file."""
    return len(PdfReader(str(pdf_path)).pages)

"""Utility functions for file operations and environment checks."""

import shutil
from pathlib import Path


def copy_template_file(src: Path, dst: Path) -> None:
    """Copy a template file from src to dst.

    Raises:
        FileNotFoundError: If src does not exist.
        FileExistsError: If dst already exists.
    """
    if not src.is_file():
        raise FileNotFoundError(f"Template not found: {src}")
    if dst.exists():
        raise FileExistsError(f"File already exists: {dst}")
    shutil.copy2(src, dst)


def check_playwright_browser() -> bool:
    """Check if Playwright Chromium browser is installed."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        return True
    except Exception:
        return False

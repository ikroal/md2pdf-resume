"""CLI entry point using Typer."""

from pathlib import Path

import typer

from md2pdf_resume.config import DEFAULTS, TEMPLATES_DIR, get_template_md_path
from md2pdf_resume.utils import check_playwright_browser, copy_template_file

app = typer.Typer(
    name="md2pdf-resume",
    help="Generate PDF resumes from Markdown.",
)


@app.command()
def init(
    lang: str = typer.Option(DEFAULTS["lang"], help="Language: zh or en."),
) -> None:
    """Initialize resume templates in the current directory."""
    md_src = get_template_md_path(lang)
    if md_src is None:
        typer.echo(f"Error: Unknown language: {lang}. Use 'zh' or 'en'.", err=True)
        raise typer.Exit(code=1)
    css_src = TEMPLATES_DIR / "default.css"

    md_dst = Path(str(DEFAULTS["md"]))
    css_dst = Path(str(DEFAULTS["css"]))

    try:
        copy_template_file(md_src, md_dst)
        copy_template_file(css_src, css_dst)
    except FileExistsError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Created {md_dst} and {css_dst}")
    typer.echo("Edit them, then run: md2pdf-resume generate")


@app.command()
def generate(
    md: Path = typer.Option(Path(str(DEFAULTS["md"])), help="Markdown file path."),
    css: Path = typer.Option(Path(str(DEFAULTS["css"])), help="CSS file path."),
    output: Path = typer.Option(
        None, help="Output PDF path (default: same as md with .pdf)."
    ),
    template: str = typer.Option(
        None, help="Built-in template name (overrides --css)."
    ),
) -> None:
    """Generate a PDF from Markdown and CSS."""
    if not md.is_file():
        typer.echo(f"Error: Markdown file not found: {md}", err=True)
        raise typer.Exit(code=1)

    if template:
        from md2pdf_resume.config import get_template_path

        template_css = get_template_path(template)
        if template_css is None:
            typer.echo(f"Error: Unknown template: {template}", err=True)
            raise typer.Exit(code=1)
        css = template_css
    elif not css.is_file():
        typer.echo(f"Error: CSS file not found: {css}", err=True)
        raise typer.Exit(code=1)

    if output is None:
        output = md.with_suffix(".pdf")

    if not check_playwright_browser():
        typer.echo(
            "Error: Playwright Chromium not installed.\n"
            "Run: playwright install chromium",
            err=True,
        )
        raise typer.Exit(code=1)

    from md2pdf_resume.converter import convert

    convert(md, css, output)
    typer.echo(f"Generated: {output}")

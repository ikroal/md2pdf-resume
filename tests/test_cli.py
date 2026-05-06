from pathlib import Path

from typer.testing import CliRunner

from md2pdf_resume.cli import app

runner = CliRunner()


def test_init_creates_files(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert (tmp_path / "resume.md").exists()
    assert (tmp_path / "resume.css").exists()


def test_init_en_creates_files(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["init", "--lang", "en"])

    assert result.exit_code == 0
    assert (tmp_path / "resume.md").exists()
    assert (tmp_path / "resume.css").exists()


def test_init_fails_if_files_exist(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]
    (tmp_path / "resume.md").write_text("existing")

    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0


def test_generate_missing_md_fails(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["generate"])

    assert result.exit_code != 0


def test_generate_help() -> None:
    result = runner.invoke(app, ["generate", "--help"])

    assert result.exit_code == 0
    assert "--md" in result.output
    assert "--css" in result.output
    assert "--output" in result.output

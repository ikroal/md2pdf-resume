# md2pdf-resume Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将单脚本改造为规范的 CLI 工具 `md2pdf-resume`，支持 `init` 和 `generate` 两个子命令。

**Architecture:** src layout 结构，Typer CLI 入口，模块按职责拆分（html_builder、converter、config、utils），内置模板通过 `init` 命令复制到用户目录。

**Tech Stack:** Python 3.10+, Typer, markdown, pypdf, Playwright, pytest, Ruff, mypy

---

## File Map

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | 项目元数据、依赖、scripts 入口、Ruff/mypy 配置 |
| `.gitignore` | Git 忽略规则 |
| `LICENSE` | MIT 协议 |
| `src/md2pdf_resume/__init__.py` | 包版本号 |
| `src/md2pdf_resume/config.py` | 模板目录、默认参数 |
| `src/md2pdf_resume/utils.py` | 文件操作、Playwright 检测 |
| `src/md2pdf_resume/html_builder.py` | Markdown → HTML 转换 |
| `src/md2pdf_resume/converter.py` | HTML → PDF 转换（含缩放） |
| `src/md2pdf_resume/templates/default.md` | 默认中文简历模板 |
| `src/md2pdf_resume/templates/default_en.md` | 默认英文简历模板 |
| `src/md2pdf_resume/templates/default.css` | 默认样式 |
| `src/md2pdf_resume/cli.py` | Typer CLI 入口 |
| `tests/conftest.py` | pytest fixtures |
| `tests/test_html_builder.py` | html_builder 单元测试 |
| `tests/test_converter.py` | converter 集成测试 |
| `tests/test_cli.py` | CLI 测试 |

---

### Task 1: Project Scaffolding

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `LICENSE`
- Create: `src/md2pdf_resume/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "md2pdf-resume"
version = "0.1.0"
description = "Generate PDF resumes from Markdown"
readme = "README.md"
license = "MIT"
requires-python = ">=3.10"
dependencies = [
    "typer>=0.9,<1.0",
    "markdown>=3.5,<4.0",
    "pypdf>=3.0,<5.0",
    "playwright>=1.40,<2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.3",
    "mypy>=1.8",
]

[project.scripts]
md2pdf-resume = "md2pdf_resume.cli:app"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "SIM"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "integration: marks tests as integration tests (deselect with '-m \"not integration\"')",
]
```

- [ ] **Step 2: Create .gitignore**

```
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg
.venv/
venv/
.mypy_cache/
.ruff_cache/
.pytest_cache/
*.pdf
.DS_Store
```

- [ ] **Step 3: Create LICENSE**

```text
MIT License

Copyright (c) 2026 ikroal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Create package structure**

Create `src/md2pdf_resume/__init__.py`:
```python
"""md2pdf-resume: Generate PDF resumes from Markdown."""

__version__ = "0.1.0"
```

Create `tests/__init__.py`:
```python
```

- [ ] **Step 5: Initialize git and commit**

```bash
git init
git add pyproject.toml .gitignore LICENSE src/md2pdf_resume/__init__.py tests/__init__.py
git commit -m "chore: initialize project scaffolding"
```

---

### Task 2: Config Module

**Files:**
- Create: `src/md2pdf_resume/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_config.py`:
```python
from pathlib import Path

from md2pdf_resume.config import DEFAULTS, TEMPLATES_DIR, get_template_path, get_template_md_path


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_config.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'md2pdf_resume.config'"

- [ ] **Step 3: Write implementation**

Create `src/md2pdf_resume/config.py`:
```python
"""Configuration and default values."""

from pathlib import Path

TEMPLATES_DIR: Path = Path(__file__).parent / "templates"

DEFAULTS: dict[str, str | None] = {
    "md": "resume.md",
    "css": "resume.css",
    "output": None,
    "lang": "zh",
}


def get_template_path(name: str) -> Path | None:
    """Return path to a built-in CSS template, or None if not found."""
    css_path = TEMPLATES_DIR / f"{name}.css"
    return css_path if css_path.is_file() else None


def get_template_md_path(lang: str) -> Path | None:
    """Return path to a built-in MD template for the given language."""
    if lang == "zh":
        md_path = TEMPLATES_DIR / "default.md"
    elif lang == "en":
        md_path = TEMPLATES_DIR / "default_en.md"
    else:
        return None
    return md_path if md_path.is_file() else None
```

- [ ] **Step 4: Create placeholder templates so tests pass**

Create `src/md2pdf_resume/templates/default.md` (empty placeholder):
```markdown
```

Create `src/md2pdf_resume/templates/default.css` (empty placeholder):
```css
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_config.py -v`
Expected: all PASS

- [ ] **Step 6: Commit**

```bash
git add src/md2pdf_resume/config.py src/md2pdf_resume/templates/ tests/test_config.py
git commit -m "feat: add config module with template paths and defaults"
```

---

### Task 3: Utils Module

**Files:**
- Create: `src/md2pdf_resume/utils.py`
- Create: `tests/test_utils.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_utils.py`:
```python
import shutil
from pathlib import Path

import pytest

from md2pdf_resume.utils import copy_template_file, check_playwright_browser


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_utils.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Write implementation**

Create `src/md2pdf_resume/utils.py`:
```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_utils.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/md2pdf_resume/utils.py tests/test_utils.py
git commit -m "feat: add utils module with file copy and playwright check"
```

---

### Task 4: HTML Builder Module

**Files:**
- Create: `src/md2pdf_resume/html_builder.py`
- Create: `tests/test_html_builder.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_html_builder.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_html_builder.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Write implementation**

Create `src/md2pdf_resume/html_builder.py`:
```python
"""Build complete HTML documents from Markdown and CSS."""

import markdown


def build_html(markdown_text: str, css_text: str) -> str:
    """Convert Markdown text to a complete HTML document with embedded CSS."""
    body_html = markdown.markdown(
        markdown_text, extensions=["extra", "sane_lists"]
    )
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_html_builder.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/md2pdf_resume/html_builder.py tests/test_html_builder.py
git commit -m "feat: add html_builder module for MD to HTML conversion"
```

---

### Task 5: Converter Module

**Files:**
- Create: `src/md2pdf_resume/converter.py`
- Create: `tests/test_converter.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_converter.py`:
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_converter.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Write implementation**

Create `src/md2pdf_resume/converter.py`:
```python
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
    page = await browser.new_page(
        viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT}
    )
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
    page = await browser.new_page(
        viewport={"width": PAGE_WIDTH, "height": PAGE_HEIGHT}
    )
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_converter.py -v -m integration`
Expected: all PASS (requires Playwright Chromium installed)

- [ ] **Step 5: Commit**

```bash
git add src/md2pdf_resume/converter.py tests/test_converter.py
git commit -m "feat: add converter module with auto-scaling PDF generation"
```

---

### Task 6: Default Templates

**Files:**
- Modify: `src/md2pdf_resume/templates/default.md`
- Modify: `src/md2pdf_resume/templates/default.css`

- [ ] **Step 1: Write default.md template**

Overwrite `src/md2pdf_resume/templates/default.md`:
```markdown
<!--
  简历模板 - 使用说明
  ==================
  1. 运行 `md2pdf-resume init` 生成本文件
  2. 按照下方结构填写你的真实信息
  3. 运行 `md2pdf-resume generate` 生成 PDF
  4. 删除所有注释后再生成最终版本

  格式约定：
  - h1 (#): 姓名，居中显示
  - 紧跟 h1 的段落: 联系方式行（emoji 分隔）
  - h2 (##): 大分区标题（教育/经历/技能等）
  - h3 (###): 子条目（公司/学校）
  - edu-row div: 教育背景的左右对齐布局
  - 加粗 (**): 项目名称、字段标签
  - 列表项 (-): 项目职责、技能条目
-->

# 张三

🧑‍💻 5年经验 ｜ 🔢 28岁 ｜ 📞 13800138000 ｜ 📧 zhangsan@example.com ｜ 🔗 github.com/zhangsan

## 🎓 教育背景

<!-- 教育经历：学位在左，学院专业在右，下方写时间和研究方向 -->
<div class="edu-row"><strong>某某大学（硕士）</strong><span>计算机学院 · 计算机科学与技术</span></div>
2018.09 - 2021.06 ｜ 研究方向：分布式系统

<div class="edu-row"><strong>某某大学（学士）</strong><span>信息学院 · 软件工程</span></div>
2014.09 - 2018.06

## 💼 工作经历

### 某某科技有限公司 ｜ 高级工程师
2021.07 - 至今

<!-- 每个项目按「描述 → 职责 → 成果」三段式，成果尽量量化 -->
**项目A：某某系统设计与实现（负责人）**

- **项目描述**：基于某某技术栈构建某某系统，解决某某业务问题。
- **主要职责**：负责方案设计与核心模块开发，协调跨团队协作。
- **成果**：性能提升 50%，支撑日均 100 万次请求。

**项目B：某某功能优化（参与者）**

- **项目描述**：针对现有系统某某瓶颈进行优化改造。
- **主要职责**：负责某某模块的性能分析与重构。
- **成果**：响应时间从 200ms 降至 50ms。

### 某某科技有限公司 ｜ 工程师
2017.07 - 2021.06

**项目C：某某平台搭建（负责人）**

- **项目描述**：从零搭建某某平台，支撑某某业务场景。
- **主要职责**：负责架构设计、技术选型与团队管理。
- **成果**：平台上线后支撑业务增长 3 倍。

## 🧠 专业技能

<!-- 列出你的核心技术栈，每条一行，简洁有力 -->
- 熟练掌握 Python/Go/C++ 等编程语言
- 熟悉分布式系统设计与微服务架构
- 熟悉 MySQL、Redis、Kafka 等中间件
- 熟悉 Kubernetes、Docker 等容器化技术
```

- [ ] **Step 2: Write default.css template**

Overwrite `src/md2pdf_resume/templates/default.css`:
```css
@page {
  size: A4;
  margin: 10mm 12mm;
}

:root {
  --text: #1f2937;
  --muted: #667085;
  --line: #dbe3ee;
  --accent: #2563eb;
}

html,
body {
  margin: 0;
  padding: 0;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC",
    "Source Han Sans SC", "Segoe UI", Arial, sans-serif;
}

#write {
  width: 100%;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  font-family: inherit;
  font-size: 13.4px;
  line-height: 1.45;
  color: var(--text);
}

#write h1 {
  margin: 0;
  text-align: center;
  font-size: 36px;
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: 0.5px;
}

#write h1 + p {
  margin: 4px 0 10px;
  text-align: center;
  color: #475467;
  font-size: 11.8px;
  font-weight: 500;
  line-height: 1.3;
  padding-bottom: 0;
  border-bottom: none;
}

#write .edu-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin: 2px 0;
}

#write .edu-row strong {
  font-weight: 760;
}

#write .edu-row span {
  color: #475467;
  text-align: right;
  white-space: nowrap;
}

#write h2 {
  margin: 12px 0 6px;
  padding: 3px 0 3px 9px;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  border-left: 4px solid var(--accent);
  border-bottom: 1px solid var(--line);
  page-break-after: avoid;
}

#write h3 {
  margin: 10px 0 3px;
  font-size: 15px;
  font-weight: 750;
  color: #0f172a;
  page-break-after: avoid;
}

#write h3 + p {
  margin: 0 0 6px;
  color: var(--muted);
  font-size: 12.8px;
}

#write p {
  margin: 2px 0;
}

#write strong {
  color: #0f172a;
}

#write ul {
  margin: 2px 0 7px 18px;
  padding: 0;
}

#write li {
  margin: 2px 0;
}

#write li::marker {
  color: #5b6b84;
}

#write code {
  font-family: inherit;
  background: transparent;
  padding: 0;
  border-radius: 0;
  font-size: inherit;
}

#write h3 + p + p,
#write h3 + p + p + ul,
#write h3 + p + p + ul + p,
#write h3 + p + p + ul + p + ul,
#write h2 + p,
#write h2 + p + p,
#write h2 + p + p + h3,
#write h2 + h3,
#write h2 + h3 + p,
#write h2 + h3 + p + p,
#write h2 + h3 + p + p + ul {
  break-inside: avoid;
  page-break-inside: avoid;
}

@media print {
  html,
  body {
    zoom: 1;
  }

  #write {
    width: 100% !important;
    max-width: none !important;
    margin: 0 !important;
    padding: 0 !important;
    font-size: 13.6px;
    line-height: 1.42;
  }

  #write h2 {
    font-size: 18px;
  }

  #write h3 {
    font-size: 15px;
  }

  #write p,
  #write ul,
  #write li {
    orphans: 3;
    widows: 3;
  }
}
```

- [ ] **Step 3: Write default_en.md template**

Create `src/md2pdf_resume/templates/default_en.md`:
```markdown
<!--
  Resume Template - Instructions
  ==============================
  1. Run `md2pdf-resume init --lang en` to generate this file
  2. Fill in your real information following the structure below
  3. Run `md2pdf-resume generate` to create PDF
  4. Remove all comments before generating the final version

  Format conventions:
  - h1 (#): Name, centered
  - Paragraph after h1: Contact info line (separated by |)
  - h2 (##): Major sections (Education, Experience, Skills)
  - h3 (###): Sub-entries (Company, University)
  - edu-row div: Left-right aligned layout for education
  - Bold (**): Project names, field labels
  - List items (-): Responsibilities, skills
-->

# San Zhang

🧑‍💻 5 Years Experience ｜ 📞 +86 138-0013-8000 ｜ 📧 zhangsan@example.com ｜ 🔗 github.com/zhangsan

## Education

<div class="edu-row"><strong>University of Example (M.S.)</strong><span>Computer Science</span></div>
2018.09 - 2021.06 ｜ Research: Distributed Systems

<div class="edu-row"><strong>University of Example (B.S.)</strong><span>Software Engineering</span></div>
2014.09 - 2018.06

## Experience

### Example Tech Co. ｜ Senior Engineer
2021.07 - Present

**Project A: System Design & Implementation (Lead)**

- Designed and built a distributed system using Go and Kubernetes
- Reduced latency by 50% through caching and query optimization
- Mentored 3 junior engineers and conducted code reviews

**Project B: Performance Optimization (Contributor)**

- Profiled and optimized critical database queries
- Improved throughput from 10K to 50K requests per second
- Implemented monitoring dashboards with Grafana

### Example Corp ｜ Engineer
2017.07 - 2021.06

**Project C: Platform Development (Lead)**

- Built a microservices platform from scratch serving 1M+ users
- Designed CI/CD pipelines reducing deployment time by 80%
- Led a team of 5 engineers across 2 time zones

## Skills

- Proficient in Python, Go, Java
- Experienced with distributed systems and microservices architecture
- Familiar with MySQL, Redis, Kafka, Elasticsearch
- Hands-on with Kubernetes, Docker, Terraform
```

- [ ] **Step 4: Verify config tests still pass**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_config.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/md2pdf_resume/templates/
git commit -m "feat: add default resume templates (zh + en)"
```

---

### Task 7: CLI Module

**Files:**
- Create: `src/md2pdf_resume/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing test**

Create `tests/test_cli.py`:
```python
from pathlib import Path

from typer.testing import CliRunner

from md2pdf_resume.cli import app

runner = CliRunner()


def test_init_creates_files(tmp_path: Path, monkeypatch: object) -> None:
    import os

    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["init"])

    assert result.exit_code == 0
    assert (tmp_path / "resume.md").exists()
    assert (tmp_path / "resume.css").exists()


def test_init_en_creates_files(tmp_path: Path, monkeypatch: object) -> None:
    import os

    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["init", "--lang", "en"])

    assert result.exit_code == 0
    assert (tmp_path / "resume.md").exists()
    assert (tmp_path / "resume.css").exists()


def test_init_fails_if_files_exist(tmp_path: Path, monkeypatch: object) -> None:
    import os

    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]
    (tmp_path / "resume.md").write_text("existing")

    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0


def test_generate_missing_md_fails(tmp_path: Path, monkeypatch: object) -> None:
    import os

    monkeypatch.chdir(tmp_path)  # type: ignore[attr-defined]

    result = runner.invoke(app, ["generate"])

    assert result.exit_code != 0


def test_generate_help() -> None:
    result = runner.invoke(app, ["generate", "--help"])

    assert result.exit_code == 0
    assert "--md" in result.output
    assert "--css" in result.output
    assert "--output" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_cli.py -v`
Expected: FAIL with "ModuleNotFoundError"

- [ ] **Step 3: Write implementation**

Create `src/md2pdf_resume/cli.py`:
```python
"""CLI entry point using Typer."""

from pathlib import Path

import typer

from md2pdf_resume.config import DEFAULTS, TEMPLATES_DIR, get_template_md_path
from md2pdf_resume.utils import copy_template_file, check_playwright_browser

app = typer.Typer(
    name="md2pdf-resume",
    help="Generate PDF resumes from Markdown.",
)


@app.command()
def init(
    lang: str = typer.Option(
        DEFAULTS["lang"], help="Language: zh or en."
    ),
) -> None:
    """Initialize resume templates in the current directory."""
    md_src = get_template_md_path(lang)
    if md_src is None:
        typer.echo(f"Error: Unknown language: {lang}. Use 'zh' or 'en'.", err=True)
        raise typer.Exit(code=1)
    css_src = TEMPLATES_DIR / "default.css"

    md_dst = Path(DEFAULTS["md"])  # type: ignore[arg-type]
    css_dst = Path(DEFAULTS["css"])  # type: ignore[arg-type]

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
    md: Path = typer.Option(
        Path(DEFAULTS["md"]),  # type: ignore[arg-type]
        help="Markdown file path.",
    ),
    css: Path = typer.Option(
        Path(DEFAULTS["css"]),  # type: ignore[arg-type]
        help="CSS file path.",
    ),
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/test_cli.py -v`
Expected: all PASS

- [ ] **Step 5: Commit**

```bash
git add src/md2pdf_resume/cli.py tests/test_cli.py
git commit -m "feat: add CLI with init and generate commands"
```

---

### Task 8: Code Quality Setup

**Files:**
- Modify: `pyproject.toml` (already has Ruff/mypy config)

- [ ] **Step 1: Install dev dependencies**

Run: `cd /Users/ikroal/Data/code/resume && pip install -e ".[dev]"`
Expected: successful install

- [ ] **Step 2: Run Ruff format**

Run: `cd /Users/ikroal/Data/code/resume && ruff format src/ tests/`
Expected: files formatted

- [ ] **Step 3: Run Ruff lint**

Run: `cd /Users/ikroal/Data/code/resume && ruff check src/ tests/`
Expected: no errors (fix any that appear)

- [ ] **Step 4: Run mypy**

Run: `cd /Users/ikroal/Data/code/resume && mypy src/`
Expected: "Success: no issues found"

- [ ] **Step 5: Run all tests**

Run: `cd /Users/ikroal/Data/code/resume && python -m pytest tests/ -v -m "not integration"`
Expected: all PASS

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: apply ruff formatting and fix lint issues"
```

---

### Task 9: Final Cleanup

**Files:**
- Delete: `generate_resume_pdf.py` (old single script)
- Delete: `resume_template.md` (old template)
- Delete: `resume.css` (old CSS, replaced by template)
- Create: `README.md`

- [ ] **Step 1: Remove old files**

```bash
rm generate_resume_pdf.py resume_template.md resume.css
```

- [ ] **Step 2: Create README.md**

```markdown
# md2pdf-resume

Generate PDF resumes from Markdown.

## Install

```bash
pip install -e .
playwright install chromium
```

## Usage

```bash
# Initialize templates (Chinese)
md2pdf-resume init

# Initialize templates (English)
md2pdf-resume init --lang en

# Edit resume.md and resume.css, then generate
md2pdf-resume generate

# Custom paths
md2pdf-resume generate --md my_resume.md --css style.css --output my_resume.pdf

# Use built-in template
md2pdf-resume generate --md resume.md --template default
```

## Development

```bash
pip install -e ".[dev]"
pytest -m "not integration"
ruff format src/ tests/
ruff check src/ tests/
mypy src/
```
```

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "chore: remove old script, add README"
```

---

## Verification

1. Run unit tests: `python -m pytest tests/ -v -m "not integration"`
2. Run integration tests: `python -m pytest tests/ -v -m integration`
3. Run lint: `ruff check src/ tests/`
4. Run format check: `ruff format --check src/ tests/`
5. Run type check: `mypy src/`
6. Manual test: `md2pdf-resume init && md2pdf-resume generate`

# md2pdf-resume CLI 工具设计文档

## Context

当前项目是一个单脚本（`generate_resume_pdf.py`），将 Markdown 简历转换为 PDF。存在以下问题：
- 所有路径硬编码，不可配置
- 无依赖管理（无 `requirements.txt`、无 `pyproject.toml`）
- 无版本控制、无开源协议
- 存在死代码（`strip_line_prefixes`）
- 不符合 Python 项目规范

目标：将其改造为一个规范的 CLI 工具 `md2pdf-resume`，支持初始化模板和生成 PDF 两个子命令。

## 项目结构

```
md2pdf-resume/
├── src/
│   └── md2pdf_resume/
│       ├── __init__.py
│       ├── cli.py              # Typer 入口，参数解析
│       ├── converter.py        # MD → HTML → PDF 核心逻辑
│       ├── html_builder.py     # HTML 模板构建
│       ├── config.py           # 配置管理（默认值、模板路径）
│       ├── templates/
│       │   ├── default.md      # 默认简历模板
│       │   └── default.css     # 默认样式
│       └── utils.py            # 工具函数
├── tests/
│   ├── test_cli.py
│   ├── test_converter.py
│   └── test_html_builder.py
├── pyproject.toml
├── LICENSE
├── .gitignore
└── README.md
```

采用 **src layout**，代码放在 `src/md2pdf_resume/` 下。

## CLI 接口

### `init` 子命令

在当前目录生成模板文件，供用户编辑后使用。

```bash
md2pdf-resume init [--lang zh|en]
```

- `--lang zh`（默认）：生成中文模板 `resume.md` + `resume.css`
- `--lang en`：生成英文模板
- 从内置 `templates/` 目录复制文件到当前目录
- 若文件已存在，提示用户确认覆盖

### `generate` 子命令

从 Markdown 和 CSS 生成 PDF。

```bash
md2pdf-resume generate [--md resume.md] [--css resume.css] [--output out.pdf] [--template default]
```

- `--md`：MD 文件路径，默认 `resume.md`
- `--css`：CSS 文件路径，默认 `resume.css`
- `--output`：输出 PDF 路径，默认与 MD 文件同名（`.pdf` 后缀）
- `--template`：使用内置样式（如 `default`），指定后忽略 `--css`

**依赖检查：** 运行时检测 Playwright Chromium 是否安装，未安装则提示 `playwright install chromium`。

## 模块职责

### `cli.py`

- 定义 Typer `app`，注册 `init` 和 `generate` 子命令
- 参数解析和校验
- 调用其他模块完成实际工作
- 错误处理和用户友好提示

### `html_builder.py`

- `build_html(markdown_text: str, css_text: str) -> str`
- 将 Markdown 转为 HTML body（使用 `markdown` 库，extensions: `extra`, `sane_lists`）
- 拼装完整 HTML 文档（DOCTYPE、charset、CSS、`#write` 容器）

### `converter.py`

- `measure_scale(html: str) -> float`：测量内容高度，计算缩放比例（0.72 ~ 1.0）
- `generate_pdf(html: str, output: Path, scale: float) -> None`：调用 Playwright 生成 PDF
- `convert(md_path: Path, css_path: Path, output: Path) -> None`：主流程入口
  - 读取 MD/CSS 文件
  - 调用 `html_builder` 构建 HTML
  - 测量缩放比例
  - 生成 PDF，若超过一页则逐步缩小 scale（0.72 → 0.55，步长 0.03）
  - 浏览器实例复用（`measure_scale` 和 `generate_pdf` 共用）

### `config.py`

- `TEMPLATES_DIR`：内置模板目录路径
- `DEFAULTS`：默认参数字典
- 提供获取内置模板路径的辅助函数

### `utils.py`

- 文件操作辅助函数（安全复制、路径处理等）
- Playwright 可用性检测

## 依赖与打包

```toml
[project]
name = "md2pdf-resume"
version = "0.1.0"
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
```

## 代码规范

- **Ruff**：格式化 + lint，配置在 `pyproject.toml` 的 `[tool.ruff]`
- **mypy**：严格模式，配置在 `pyproject.toml` 的 `[tool.mypy]`
- **命名**：函数 `snake_case`，类 `PascalCase`，常量 `UPPER_CASE`
- **类型注解**：所有公开函数签名必须有类型注解
- **函数长度**：不超过 50 行
- **圈复杂度**：不超过 20
- **函数参数**：不超过 5 个

## 测试策略

- `test_html_builder.py`：测试 MD → HTML 转换，检查输出结构和 CSS 注入
- `test_converter.py`：测试 PDF 生成（需 Playwright，标记为 `@pytest.mark.integration`）
- `test_cli.py`：测试 CLI 参数解析和命令调用（用 Typer 的 `CliRunner`）

## 开源协议

MIT License

# Markup+

> A modern markup language with more features than Markdown

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](https://github.com/USERNAME/markup-plus/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](tests/)

**Markup+** is a modern markup language that extends Markdown with powerful
features for building documentation, blogs, reports, and interactive web pages.

Everything you know from Markdown still works -- you just get more powerful
features on top.

---

## ✨ Why Markup+?

| Feature | Markdown | Markup+ |
|---------|:--------:|:-------:|
| Headings, lists, tables | Yes | Yes |
| Bold, italic, links, images | Yes | Yes |
| Footnotes | Partial | Yes |
| Variables | No | Yes |
| Conditionals (`@if`) | No | Yes |
| Loops (`@each`) | No | Yes |
| Reusable components | No | Yes |
| Charts (bar, line, pie, doughnut) | No | Yes |
| Math formulas (KaTeX) | No | Yes |
| Tabs & accordions | No | Yes |
| Rich alerts (note, warning, tip, danger, success) | No | Yes |
| Auto RTL detection (Persian, Arabic, Hebrew) | No | Yes |
| Light & dark themes | No | Yes |
| Rich code blocks (copy, download, preview) | No | Yes |
| Image galleries with lightbox | No | Yes |
| File imports (`@import`) | No | Yes |

---

## 🚀 Quick Start

### Install

```bash
pip install markup-plus
```

### Create your first document

```bash
mup new hello
```

This creates `hello.mup`:

```mup
# Hello World

This is **bold** text.
```

### Convert to HTML

```bash
mup hello.mup
```

Opens `hello.html` in your browser. Done!

---

## 📖 Example

```mup
---
title: My Article
author: Ali
---

# {title}

By **{author}**

@let fruits = ["Apple", "Banana", "Cherry"]

## Fruits

@each fruit in fruits
- {fruit}
@end

@note
This is a note box.
@end

@chart(type="bar")
data: [10, 20, 30]
labels: ["A", "B", "C"]
@end
```

**Output:** A beautiful HTML page with variable substitution, a
loop-generated list, a styled note box, and an interactive chart.

---

## 🎯 Features

### Core (Markdown-compatible)

- Headings (H1-H6)
- **Bold**, *italic*, ~~strikethrough~~
- Inline code and code blocks
- Lists (ordered, unordered, task lists)
- Blockquotes, horizontal rules
- Links, images, autolinks
- Tables with alignment
- Footnotes

### Advanced

- **Variables** -- `@let name = "Ali"`
- **Filters** -- `{name | upper}`, `{name | reverse}`
- **Conditionals** -- `@if`, `@elif`, `@else`
- **Loops** -- `@each item in items`
- **Components** -- `@def Card(title, body)` + `@Card(title="Hi")`
- **Imports** -- `@import "header.mup"`
- **Table of Contents** -- `@toc`

### Rich Content

- **Charts** -- bar, line, pie, doughnut (Chart.js)
- **Math** -- inline `$x^2$` and block `$$ E = mc^2 $$` (KaTeX)
- **Tabs** -- `@tabs` + `@tab "Title"`
- **Accordions** -- `@collapse` + `@item "Question"`
- **Alerts** -- `@note`, `@warning`, `@tip`, `@danger`, `@success`
- **Quotes** -- `@quote(author="...")`
- **Timelines** -- `@timeline`

### Experience

- Light/Dark themes
- Auto RTL detection (Persian, Arabic, Hebrew)
- Responsive design
- Smooth animations
- Image lightbox with zoom
- Rich code blocks (copy, download, preview)

---

## 📚 Documentation

- **[User Guide](GUIDE.md)** -- Complete syntax reference
- **[Tutorial](TUTORIAL.md)** -- Step-by-step from zero to hero
- **[Developer Guide](DEVELOPER.md)** -- Architecture & contribution
- **[Roadmap](ROADMAP.md)** -- What's coming next
- **[Changelog](CHANGELOG.md)** -- Version history
- **[Contributing](CONTRIBUTING.md)** -- How to contribute

---

## 🖥️ CLI

```bash
mup <file>              # Convert .mup or .md to HTML
mup new <name>          # Create a new .mup file
mup check <file>        # Validate a file
mup open <file>         # View in terminal with highlighting
mup init [name]         # Initialize a project
mup --dark <file>       # Dark theme
mup --rtl <file>        # Force RTL layout
mup --help              # Show help
```

### Options

| Option | Description |
|--------|-------------|
| `-d, --dark` | Use dark theme |
| `-l, --light` | Use light theme (default) |
| `-r, --rtl` | Force right-to-left layout |
| `--ltr` | Force left-to-right layout |
| `-o, --output <file>` | Custom output file path |
| `--debug` | Show debug info |
| `-h, --help` | Show help |
| `-v, --version` | Show version |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src/markup_plus --cov-report=html
```

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md)
first.

```bash
git clone https://github.com/USERNAME/markup-plus.git
cd markup-plus
pip install -e .
pip install pytest pytest-cov black ruff
pytest tests/ -v
```

---

## 📦 Project Structure

```
markup-plus/
|-- src/markup_plus/
|   |-- __init__.py         # Public API
|   |-- __main__.py         # python -m entry
|   |-- ast.py              # AST nodes
|   |-- errors.py           # Custom exceptions
|   |-- lexer.py            # Tokenizer
|   |-- parser.py           # Parser
|   |-- renderer.py         # HTML renderer
|   `-- cli/                # Command-line interface
|-- tests/                  # Test suite
|-- examples/               # Example .mup files
|-- docs/                   # Documentation
`-- assets/                 # Static assets
```

---

## 🌟 Star History

If Markup+ helps you, please give it a star!

---

## 📜 License

MIT (c) 2025 Ataee -- free to use, modify, and distribute.

See [LICENSE](LICENSE) for details.

---

**Made with love using Markup+ v0.6.0**
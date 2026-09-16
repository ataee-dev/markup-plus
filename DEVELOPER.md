# 🛠️ Markup+ — Developer Guide

> **Version:** 0.6.0
> **Audience:** Developers contributing to or extending Markup+
> **Prerequisites:** Python 3.9+, familiarity with lexers/parsers

Complete technical documentation for the Markup+ codebase.

---

## 📑 Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Project Structure](#2-project-structure)
3. [Processing Pipeline](#3-processing-pipeline)
4. [Module Reference](#4-module-reference)
5. [Adding a New Directive](#5-adding-a-new-directive)
6. [Testing](#6-testing)
7. [CLI Development](#7-cli-development)
8. [Release Process](#8-release-process)
9. [Performance](#9-performance)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Architecture Overview

Markup+ follows a classic **compiler pipeline**:

```
┌─────────────────┐
│  Source Text    │   .mup file (or .md)
│  (string)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Lexer          │   lexer.py — line-based tokenizer
│                 │   Output: List[Token]
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Parser         │   parser.py — recursive descent
│                 │   Output: Document (AST)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Import         │   renderer.resolve_imports()
│  Resolver       │   Loads @import files
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Evaluator      │   renderer.evaluate_*() — conditions, loops
│  (part of       │   Variables, filters, @if, @each
│   renderer)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Renderer       │   renderer.py — AST → HTML
│                 │   Output: HTML string
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTML Template  │   HEAD + body + TAIL
│  Wrapper        │   Includes CSS, JS, CDN links
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output         │   .html file
└─────────────────┘
```

### Design Principles

1. **Simplicity** — line-based lexing, no complex state machines
2. **Predictability** — deterministic output, no hidden behavior
3. **Extensibility** — new directives are easy to add
4. **Separation of concerns** — lexer, parser, renderer are independent
5. **Zero config** — sensible defaults, works out of the box

### Key Decisions

| Decision | Reason |
|----------|--------|
| Line-based lexer | Markup is line-oriented; simpler than char-based |
| Recursive descent parser | Natural fit for nested blocks |
| Dataclasses for AST | Type hints, immutability, less boilerplate |
| Single renderer file | Simpler imports, no circular deps |
| Evaluator in renderer | Small codebase; splitting adds complexity |
| CDN for libraries | No bundled dependencies, smaller output |

---

## 2. Project Structure

```
markup-plus/
│
├── README.md                   # Project overview
├── GUIDE.md                    # User manual (Markdown)
├── TUTORIAL.md                 # Step-by-step tutorial
├── DEVELOPER.md                # This file
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── ROADMAP.md                  # Future plans
├── LICENSE                     # MIT
├── SECURITY.md                 # Security policy
├── pyproject.toml              # Package config
├── requirements.txt            # Dependencies
│
├── .github/                    # GitHub config
│   ├── workflows/              # CI/CD
│   │   ├── test.yml
│   │   └── publish.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── src/
│   └── markup_plus/
│       ├── __init__.py         # Public API
│       ├── __main__.py         # python -m entry
│       ├── ast.py              # AST node definitions
│       ├── errors.py           # Custom exceptions
│       ├── lexer.py            # Tokenizer
│       ├── parser.py           # Parser
│       ├── renderer.py         # HTML renderer + evaluator
│       └── cli/                # Command-line interface
│           ├── __init__.py     # Main entry
│           ├── commands.py     # Command implementations
│           ├── display.py      # Terminal viewer
│           ├── errors.py       # Error display
│           ├── theme.py        # Terminal colors
│           └── __main__.py     # python -m markup_plus.cli
│
├── tests/                      # Test suite
│   ├── test_parser.py
│   ├── test_renderer.py
│   ├── test_code.py
│   ├── test_images.py
│   ├── test_lists.py
│   ├── test_quotes.py
│   ├── test_tables.py
│   ├── test_phase3.py
│   ├── test_phase4.py
│   └── fixtures/               # Test data
│
├── examples/                   # Example .mup files
├── docs/                       # Documentation source
└── assets/                     # Static assets
    ├── css/
    ├── images/
    └── templates/
```

---

## 3. Processing Pipeline

### Example Input

```mup
---
title: Demo
---

# Hello {name}

@let name = "Ali"

@if version > 1
New version!
@endif
```

### Step 1: Lexing

`lexer.py` splits by lines and produces tokens:

```python
[
    Token(type="LINE", value="---",                    line=1),
    Token(type="LINE", value="title: Demo",             line=2),
    Token(type="LINE", value="---",                    line=3),
    Token(type="LINE", value="",                        line=4),
    Token(type="LINE", value="# Hello {name}",          line=5),
    Token(type="LINE", value="",                        line=6),
    Token(type="LINE", value='@let name = "Ali"',      line=7),
    Token(type="LINE", value="",                        line=8),
    Token(type="LINE", value="@if version > 1",         line=9),
    Token(type="LINE", value="New version!",            line=10),
    Token(type="LINE", value="@endif",                  line=11),
    Token(type="EOF",  value="",                        line=12),
]
```

### Step 2: Parsing

`parser.py` builds an AST:

```python
Document(
    meta={"title": "Demo"},
    children=[
        Heading(level=1, text="Hello {name}", line=5, slug="hello-name"),
        VariableDef(name="name", value="Ali", raw_value='"Ali"', line=7),
        IfBlock(
            branches=[("version > 1", [Paragraph(text="New version!", line=10)])],
            line=9,
        ),
    ],
    variables={"name": "Ali"},
)
```

### Step 3: Import Resolution

`renderer.resolve_imports()` replaces `ImportBlock` nodes with parsed children
of imported files (recursively).

### Step 4: Rendering

`renderer.render_ast()` walks the AST, evaluates conditions and loops, and
produces HTML:

```python
context = {"title": "Demo", "name": "Ali"}
# Note: version is undefined → condition "version > 1" is False
# So IfBlock renders nothing
```

Output body:

```html
<h1 id="hello-name" class="reveal">Hello Ali</h1>
```

### Step 5: Template Wrapping

`to_html()` wraps the body in `HEAD + body + TAIL`:

```html
<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light">
<head>...</head>
<body class="ltr">
    <h1 id="hello-name" class="reveal">Hello Ali</h1>
    <!-- TAIL: lightbox, scripts -->
</body>
</html>
```

---

## 4. Module Reference

### 4.1 `ast.py` — Node Definitions

All AST nodes are dataclasses inheriting from `Node`:

```python
@dataclass
class Node:
    line: int = 0  # Source line number for error reporting
```

**Node categories:**

| Category | Nodes |
|----------|-------|
| **Document** | `Document` |
| **Text blocks** | `Heading`, `Paragraph`, `BlockQuote`, `HorizontalRule` |
| **Lists** | `ListBlock` |
| **Code** | `CodeBlock` |
| **Images** | `ImageBlock`, `GalleryBlock` |
| **Tables** | `TableBlock` |
| **Navigation** | `TOCBlock` |
| **Logic** | `IfBlock`, `EachBlock`, `VariableDef` |
| **Components** | `ComponentDef`, `ComponentCall` |
| **Rich content** | `ChartBlock`, `MathBlock`, `TabsBlock`, `CollapseBlock`, `AlertBlock`, `QuoteBlock`, `TimelineBlock` |
| **Imports** | `ImportBlock` |

**Adding a new node:**

```python
@dataclass
class BadgeBlock(Node):
    """@badge(text="...", color="...")"""
    text: str = ""
    color: str = "blue"
```

### 4.2 `lexer.py` — Tokenizer

Minimal implementation — splits text by lines:

```python
class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")

    def tokenize(self) -> List[Token]:
        tokens = []
        for i, line in enumerate(self.lines, start=1):
            tokens.append(Token(type="LINE", value=line, line=i))
        tokens.append(Token(type="EOF", value="", line=len(self.lines) + 1))
        return tokens
```

**Why so simple?**

Markup+ is line-oriented. Almost every construct is a full line
(`# Heading`, `@if ...`, `- item`). Only inline formatting
(`**bold**`, `` `code` ``) is parsed later by regex in the renderer.

**Extensions possible:**

- State machine for multi-line blocks
- Character-level tokens for better error messages
- Syntax highlighting tokens

### 4.3 `parser.py` — Parser

The heart of the parser is `_parse_blocks()`:

```python
def _parse_blocks(self, stop_at: set) -> List:
    children = []
    while not self._is_at_end():
        # Check stop keywords (@elif, @else, @endif, @end)
        # Try each directive pattern in order
        # If match → call specific parser
        # Else → fallback to Paragraph
    return children
```

**Regex patterns** at the top of the file define what to match:

```python
RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_LET = re.compile(r"^@let\s+([A-Za-z_][\w]*)\s*=\s*(.+?)\s*$")
RE_IF = re.compile(r"^@if\s+(.+?)\s*$")
RE_CHART = re.compile(r"^@chart\s*(?:[\(\{]([^\)\}]*)[\)\}])?\s*$")
# ... etc
```

**Order matters** — more specific patterns first:

1. Stop keywords (`@endif`, `@end`)
2. Comments (`@#`)
3. `@let` (variable definitions)
4. `@def` (component definitions)
5. `@import`
6. `@if`, `@each`
7. Block directives (`@chart`, `@tabs`, `@collapse`, `@note`, ...)
8. Code fences
9. Gallery
10. TOC
11. Tables
12. Images
13. Horizontal rules
14. Headings
15. Blockquotes
16. Task lists
17. Unordered lists
18. Ordered lists
19. Component calls (`@Name(...)`)
20. Paragraph (fallback)

**Variable scope:**

The parser tracks variable definitions in `self._variables`, which are
saved to `doc.variables` at the end.

**Heading slugs:**

```python
def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\u0600-\u06FF\u0750-\u077F\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-") or "section"
```

Supports Persian (`\u0600-\u06FF`) and Arabic Supplement (`\u0750-\u077F`).

**Value parsing:**

`_parse_value()` handles:
- Strings (with or without quotes)
- Integers
- Floats
- Booleans (`true` / `false`)
- Null (`null` / `none`)
- Arrays (`[...]`)

**Top-level splitting:**

`_split_top_level()` splits by comma, ignoring commas inside brackets or quotes.
Used for arrays and component arguments.

### 4.4 `renderer.py` — Renderer

The largest module. Two parts:

#### Part A: Pure rendering functions

- `render_inline(text)` — bold, italic, links, code, math
- `render_code_block(node)` — code with header/buttons
- `render_image(node)` — with lightbox
- `render_gallery(node)` — grid with lightbox
- `render_table(node, context)` — with alignment
- `render_toc(node, doc)` — from headings
- `render_footnotes(doc)` — bottom section
- `render_node(node, doc, context)` — dispatcher

#### Part B: Evaluator functions

- `evaluate_condition(expr, variables)` — for `@if`
- `evaluate_iterable(expr, variables)` — for `@each`
- `apply_filters(value, filters)` — for `{var|upper}`
- `substitute_variables(text, variables)` — replace `{var}`

**Note:** The evaluator is intentionally part of `renderer.py`. In a
larger codebase, it would be in `evaluator.py`. For Markup+, keeping it
here reduces cross-module dependencies.

#### Part C: Template constants

- `HEAD` — everything from `<!DOCTYPE html>` to `<body>`
- `TAIL` — from `</body>` closing, includes lightbox HTML and all JS

**CSS** is embedded in `HEAD` as `<style>...</style>`.
**JS** is embedded in `TAIL` as `<script>...</script>`.

This ensures single-file output — no external assets needed.

#### Part D: Public API

```python
def to_html(
    text: str,
    title: str = "Markup+ Document",
    theme: str = "light",
    direction: str = None,
    base_dir: str = None,
) -> str:
    ...
```

Flow:

1. `parse_text(text)` → `Document`
2. `resolve_imports(doc, base_dir)` → in-place modification
3. `render_ast(doc)` → HTML body
4. Determine direction (auto or explicit)
5. Wrap in `HEAD + body + TAIL`

**RTL detection:**

```python
def is_rtl_text(text: str) -> bool:
    rtl_count = 0
    ltr_count = 0
    for char in text:
        if not char.isalpha():
            continue
        bidi = unicodedata.bidirectional(char)
        if bidi in ("R", "AL", "AN"):
            rtl_count += 1
        elif bidi == "L":
            ltr_count += 1
    total = rtl_count + ltr_count
    if total == 0:
        return False
    return (rtl_count / total) >= 0.3
```

Threshold: **30% RTL characters** → document becomes RTL.

### 4.5 `errors.py` — Exceptions

```python
class MarkupError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0):
        ...

class LexerError(MarkupError): pass
class ParserError(MarkupError): pass
class RenderError(MarkupError): pass
class EvaluationError(MarkupError): pass
```

All exceptions include line numbers for error reporting.

### 4.6 `cli/` — Command-Line Interface

**`cli/__init__.py`** — main entry point:

- Parses global flags (`--dark`, `--rtl`, `-o`, `--debug`)
- Dispatches to commands (`new`, `open`, `check`, `init`)
- Falls back to `build_file` for file paths

**`cli/commands.py`** — command implementations:

- `build_file()` — main conversion
- `new_file()` — create with template
- `open_file()` — terminal viewer
- `check_file()` — validator
- `init_project()` — project scaffold

**`cli/display.py`** — terminal syntax highlighting for `.mup`

**`cli/theme.py`** — ANSI color helpers, `supports_color()` detection

**`cli/errors.py`** — formatted error display, source context

---

## 5. Adding a New Directive

Let's walk through adding `@badge` step-by-step.

### Step 1: Design the Syntax

```mup
@badge(text="NEW", color="red")
```

Output:

```html
<span class="badge badge-red">NEW</span>
```

### Step 2: Add AST Node

**File:** `src/markup_plus/ast.py`

```python
@dataclass
class BadgeBlock(Node):
    """@badge(text="...", color="...")"""
    text: str = ""
    color: str = "blue"
```

### Step 3: Add Regex Pattern

**File:** `src/markup_plus/parser.py`

At the top with other patterns:

```python
RE_BADGE = re.compile(r'^@badge\s*(?:[\(\{]([^\)\}]*)[\)\}])?\s*$')
```

### Step 4: Add Parser Handler

**File:** `src/markup_plus/parser.py`, in `_parse_blocks()`:

```python
# Add this BEFORE the fallback to Paragraph:
m = RE_BADGE.match(stripped)
if m:
    options = self._parse_inline_options(m.group(1) or "")
    children.append(BadgeBlock(
        text=options.get("text", ""),
        color=options.get("color", "blue"),
        line=token.line,
    ))
    self._advance()
    continue
```

Add `BadgeBlock` to imports:

```python
from .ast import (
    ...
    BadgeBlock,
    ...
)
```

### Step 5: Add Renderer

**File:** `src/markup_plus/renderer.py`:

```python
def render_badge(node: BadgeBlock, context: dict) -> str:
    """Render a badge span."""
    text = substitute_variables(node.text, context)
    color = node.color or "blue"
    return (
        f'<span class="badge badge-{html.escape(color)}">'
        f'{html.escape(text)}'
        f'</span>'
    )
```

Add dispatch in `render_node()`:

```python
if isinstance(node, BadgeBlock):
    return render_badge(node, context)
```

Add `BadgeBlock` to imports:

```python
from .ast import (
    ...
    BadgeBlock,
    ...
)
```

### Step 6: Add CSS

**File:** `src/markup_plus/renderer.py`, in the `HEAD` constant, in `<style>`:

```css
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 600;
    margin: 0 4px;
}

.badge-blue   { background: #3b82f6; color: white; }
.badge-red    { background: #ef4444; color: white; }
.badge-green  { background: #10b981; color: white; }
.badge-yellow { background: #f59e0b; color: white; }
.badge-purple { background: #7c3aed; color: white; }
```

### Step 7: Write Tests

**File:** `tests/test_badge.py`:

```python
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html
from markup_plus.ast import BadgeBlock


def test_badge_parses():
    doc = parse_text('@badge(text="New", color="red")')
    assert len(doc.children) == 1
    assert isinstance(doc.children[0], BadgeBlock)
    assert doc.children[0].text == "New"
    assert doc.children[0].color == "red"


def test_badge_renders():
    html = to_html('@badge(text="New", color="red")')
    assert 'class="badge badge-red"' in html
    assert ">New</span>" in html


def test_badge_default_color():
    html = to_html('@badge(text="Hi")')
    assert "badge-blue" in html
```

### Step 8: Update Documentation

- `GUIDE.md` — add section
- `CHANGELOG.md` — add under `[Unreleased]` → `Added`
- `examples/` — add example file
- `README.md` — maybe mention

### Step 9: Run Tests

```bash
pytest tests/test_badge.py -v
pytest tests/ -v  # Full suite
```

### Step 10: Commit

```bash
git add .
git commit -m "feat: add @badge directive"
git push origin feature/add-badge
```

---

## 6. Testing

### Test Structure

```
tests/
├── test_parser.py      # Parser unit tests
├── test_renderer.py    # Renderer unit tests
├── test_code.py        # Code block tests
├── test_images.py      # Image tests
├── test_lists.py       # List tests
├── test_quotes.py      # Quote tests
├── test_tables.py      # Table tests
├── test_phase3.py      # Phase 3 features
├── test_phase4.py      # Phase 4 features
└── fixtures/           # Test data files
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# One file
pytest tests/test_parser.py -v

# One test
pytest tests/test_parser.py::test_heading -v

# With coverage
pytest tests/ --cov=src/markup_plus --cov-report=html

# Stop at first failure
pytest tests/ -x

# Verbose with print statements
pytest tests/ -v -s
```

### Test Pattern (AAA)

```python
def test_variable_substitution():
    # Arrange
    source = '@let name = "Ali"\n\nHello {name}!'

    # Act
    html = to_html(source)

    # Assert
    assert "Hello Ali!" in html
    assert "{name}" not in html
```

### Coverage

Target: **80%+**

```bash
pytest tests/ --cov=src/markup_plus --cov-report=term-missing
```

### Fixtures

Use `tests/fixtures/` for larger test files:

```python
from pathlib import Path

def test_full_document():
    source = Path("tests/fixtures/basic.mup").read_text()
    html = to_html(source)
    assert "<h1" in html
```

---

## 7. CLI Development

### Entry Point

`src/markup_plus/cli/__init__.py`:

```python
def main() -> int:
    args = sys.argv[1:]
    # Parse flags
    # Dispatch commands
    # Return exit code
```

### Adding a New Command

**Step 1:** Add to `HELP_TEXT` in `cli/__init__.py`.

**Step 2:** Dispatch in `main()`:

```python
if command == "mycmd":
    return commands.my_command(command_args)
```

**Step 3:** Implement in `cli/commands.py`:

```python
def my_command(args: list) -> int:
    """Do something useful."""
    show_success("Done!")
    return 0
```

### Terminal Colors

Use `cli/theme.py`:

```python
from . import theme

print(theme.success("Operation completed"))
print(theme.error("Something went wrong"))
print(theme.warning("Be careful"))
print(theme.info("For your information"))
```

Colors are auto-disabled when output is not a TTY or `NO_COLOR` env is set.

---

## 8. Release Process

### Version Bump

1. Update `pyproject.toml`:
   ```toml
   version = "0.7.0"
   ```

2. Update `src/markup_plus/__init__.py`:
   ```python
   __version__ = "0.7.0"
   ```

3. Update `CHANGELOG.md` — move `[Unreleased]` to `[0.7.0]`.

### Build

```bash
pip install build
python -m build
```

Creates:
- `dist/markup_plus-0.7.0.tar.gz`
- `dist/markup_plus-0.7.0-py3-none-any.whl`

### Test the Build

```bash
pip install dist/markup_plus-0.7.0-py3-none-any.whl
mup --version
```

### Publish to PyPI

```bash
pip install twine
twine upload dist/*
```

Or to TestPyPI first:

```bash
twine upload --repository testpypi dist/*
```

### Git Tag

```bash
git add .
git commit -m "Release v0.7.0"
git tag -a v0.7.0 -m "Release v0.7.0"
git push origin master
git push origin v0.7.0
```

### GitHub Release

1. Go to GitHub → Releases → "Draft a new release"
2. Choose tag `v0.7.0`
3. Title: `v0.7.0 — Interactive Elements`
4. Description: copy from CHANGELOG
5. Attach `dist/*` if applicable
6. Publish

### Automated Release (future)

See `.github/workflows/publish.yml` — publishes on tag push.

---

## 9. Performance

### Benchmarks

Target performance:

| Document size | Time | Memory |
|---------------|------|--------|
| 100 lines | <10 ms | <5 MB |
| 1,000 lines | <50 ms | <15 MB |
| 10,000 lines | <500 ms | <100 MB |
| 100,000 lines | <5 s | <1 GB |

### Profiling

```bash
python -m cProfile -s cumtime -m markup_plus big.mup
```

### Known Bottlenecks

1. **Regex backtracking** in inline formatting on very long paragraphs
2. **Repeated string concatenation** in `render_inline()`
3. **Chart.js / KaTeX / Prism.js** loaded from CDN — first render waits on network

### Optimizations

- Cache compiled regexes (already done at module level)
- Use `str.join()` for large lists (already done)
- Streaming parser for very large files (planned v0.9.0)
- Lazy-load CDN libraries (planned v0.9.0)

---

## 10. Troubleshooting

### "Module not found" errors

```bash
pip install -e .  # Reinstall in editable mode
```

### Tests fail after changes

```bash
pytest tests/ -v --tb=long  # Full traceback
```

### Changes not reflected

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
# Or on Windows:
# for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```

### RTL not detected

Check threshold in `is_rtl_text()` — currently 30% RTL characters required.

### Chart not rendering

Open browser console (F12). Usually:
- No internet (Chart.js CDN blocked)
- Invalid data format

### Circular import

If you see `ImportError: cannot import name ...`, check `renderer.py`
imports. It imports from `.parser` lazily inside `resolve_imports()`.

---

## 📚 Further Reading

- [PEP 8](https://peps.python.org/pep-0008/) — Python style guide
- [PEP 257](https://peps.python.org/pep-0257/) — Docstring conventions
- [Semantic Versioning](https://semver.org/) — Version numbering
- [Keep a Changelog](https://keepachangelog.com/) — Changelog format
- [Conventional Commits](https://www.conventionalcommits.org/) — Commit style

---

## 🤝 Getting Help

- 📖 **Documentation:** [GUIDE.md](GUIDE.md), [TUTORIAL.md](TUTORIAL.md)
- 🐛 **Issues:** [GitHub Issues](https://github.com/USERNAME/markup-plus/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/USERNAME/markup-plus/discussions)
- 📧 **Email:** [maintainer@markupplus.dev](mailto:maintainer@markupplus.dev)

---

**Last updated:** January 2025
**Version:** 0.6.0

**Happy hacking! 💜**
# Contributing to Markup+

First off — **thank you!** 🎉

Every contribution matters: bug reports, documentation fixes, new features,
translations, or just spreading the word. This guide will help you contribute
effectively.

---

## 📑 Table of Contents

1. [Code of Conduct](#1-code-of-conduct)
2. [Ways to Contribute](#2-ways-to-contribute)
3. [Before You Start](#3-before-you-start)
4. [Setting Up Your Environment](#4-setting-up-your-environment)
5. [Development Workflow](#5-development-workflow)
6. [Coding Standards](#6-coding-standards)
7. [Writing Tests](#7-writing-tests)
8. [Writing Documentation](#8-writing-documentation)
9. [Commit Message Guidelines](#9-commit-message-guidelines)
10. [Pull Request Process](#10-pull-request-process)
11. [Reporting Bugs](#11-reporting-bugs)
12. [Suggesting Features](#12-suggesting-features)
13. [Translation Guide](#13-translation-guide)
14. [Recognition](#14-recognition)

---

## 1. Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for
everyone, regardless of:

- Age, body size, disability, ethnicity
- Gender identity, expression, or sexual orientation
- Level of experience, education
- Nationality, personal appearance, race, religion

### Our Standards

**Positive behavior includes:**

- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what's best for the community
- ✅ Showing empathy toward other community members

**Unacceptable behavior includes:**

- ❌ Trolling, insulting, or derogatory comments
- ❌ Public or private harassment
- ❌ Publishing others' private information without permission
- ❌ Any conduct that could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by opening an issue or contacting the maintainers directly. All
complaints will be reviewed and investigated promptly and fairly.

---

## 2. Ways to Contribute

You don't need to write code to contribute! Here's how:

### 🐛 Report Bugs
Found something broken? [Open an issue](#11-reporting-bugs).

### 💡 Suggest Features
Have an idea? [Start a discussion](#12-suggesting-features).

### 📝 Improve Documentation
Fix typos, clarify confusing sections, add examples.

### 🧪 Write Tests
More tests = more confidence. Even one test helps.

### 🌍 Translate
Help translate documentation or CLI messages.

### 🎨 Design
Improve CSS, icons, or UI/UX.

### 💻 Write Code
Fix bugs, add features, refactor code.

### ⭐ Spread the Word
Star the repo, share on social media, write a blog post.

### 💰 Sponsor
Support development financially (see `SPONSORS.md` if available).

---

## 3. Before You Start

### Check for Existing Work

Before starting:

1. **Search issues** — someone might already be working on it
2. **Search pull requests** — it might be done
3. **Check discussions** — it might be planned
4. **Read the roadmap** — it might be scheduled for later

### Choose the Right Task

**First-time contributors** — look for:
- Issues labeled `good first issue`
- Issues labeled `documentation`
- Issues labeled `help wanted`

**Experienced contributors** — look for:
- Issues labeled `bug`
- Issues labeled `enhancement`
- Issues labeled `performance`

### Ask First for Big Changes

For **major changes** (new features, API changes, architecture):

1. Open an issue first describing your plan
2. Wait for maintainer feedback
3. Only start coding after approval

This saves you from wasted effort if the maintainer disagrees.

For **small changes** (typos, bug fixes, docs):

Just submit a pull request — no need to ask first.

---

## 4. Setting Up Your Environment

### Prerequisites

- **Python** 3.9 or higher
- **Git** installed
- A code editor (VS Code, PyCharm, etc.)

### Step 1: Fork the Repository

Go to https://github.com/USERNAME/markup-plus and click **Fork**.

This creates `https://github.com/YOUR-USERNAME/markup-plus`.

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/markup-plus.git
cd markup-plus
```

### Step 3: Add Upstream Remote

```bash
git remote add upstream https://github.com/USERNAME/markup-plus.git
git remote -v
```

You should see:

```
origin    https://github.com/YOUR-USERNAME/markup-plus.git (fetch)
origin    https://github.com/YOUR-USERNAME/markup-plus.git (push)
upstream  https://github.com/USERNAME/markup-plus.git (fetch)
upstream  https://github.com/USERNAME/markup-plus.git (push)
```

### Step 4: Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install in Development Mode

```bash
pip install -e .
```

This installs Markup+ in editable mode — changes to source take effect
immediately.

### Step 6: Install Development Dependencies

```bash
pip install pytest pytest-cov black ruff
```

Or:

```bash
pip install -r requirements.txt
```

### Step 7: Verify Setup

```bash
pytest tests/ -v
```

All tests should pass. If not, [open an issue](#11-reporting-bugs).

```bash
mup --version
```

Should output: `Markup+ v0.6.0`

---

## 5. Development Workflow

### Step 1: Sync Your Fork

Before starting work, update your fork:

```bash
git checkout master
git fetch upstream
git merge upstream/master
git push origin master
```

### Step 2: Create a Feature Branch

Use a descriptive name:

```bash
git checkout -b feature/add-run-directive
git checkout -b fix/parser-memory-leak
git checkout -b docs/improve-guide
git checkout -b test/add-chart-tests
```

**Branch name prefixes:**

| Prefix | Use For |
|--------|---------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation |
| `test/` | Tests |
| `refactor/` | Code refactoring |
| `chore/` | Maintenance (deps, config) |

### Step 3: Make Your Changes

- Write code
- Write tests
- Update docs
- Run tests locally

### Step 4: Test Your Changes

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_parser.py -v

# Run specific test
pytest tests/test_parser.py::test_heading -v

# With coverage
pytest tests/ --cov=src/markup_plus --cov-report=html
```

### Step 5: Format Your Code

```bash
# Format with black
black src/ tests/

# Lint with ruff
ruff check src/ tests/

# Auto-fix issues
ruff check src/ tests/ --fix
```

### Step 6: Commit Your Changes

```bash
git add .
git commit -m "feat: add @run directive for code blocks"
```

See [Commit Message Guidelines](#9-commit-message-guidelines) below.

### Step 7: Push to Your Fork

```bash
git push origin feature/add-run-directive
```

### Step 8: Open a Pull Request

Go to your fork on GitHub. You'll see a banner: **"Compare & pull request"**.

Click it and follow the [Pull Request Process](#10-pull-request-process).

---

## 6. Coding Standards

### Python Style

We follow **PEP 8** with some modifications:

- **Line length:** 100 characters (not 79)
- **Quotes:** Double quotes preferred
- **Indentation:** 4 spaces
- **Naming:** `snake_case` for functions, `PascalCase` for classes

### Formatting Tools

We use **black** for formatting and **ruff** for linting.

**Setup:**

```bash
pip install black ruff
```

**Run before commit:**

```bash
black src/ tests/
ruff check src/ tests/
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Module | `snake_case` | `renderer.py` |
| Class | `PascalCase` | `class Heading(Node)` |
| Function | `snake_case` | `def render_heading()` |
| Variable | `snake_case` | `heading_text = "..."` |
| Constant | `UPPER_SNAKE` | `MAX_HEADING_LEVEL = 6` |
| Private | `_leading_underscore` | `def _parse_front_matter()` |
| AST Node | `PascalCase` | `class Paragraph(Node)` |

### Docstrings

Use **Google-style docstrings** for public APIs:

```python
def render_heading(node: Heading, context: dict) -> str:
    """Render a heading to HTML.

    Args:
        node: The heading AST node.
        context: Variable context for substitution.

    Returns:
        HTML string like `<h1 id="...">Title</h1>`.

    Raises:
        RenderError: If heading level is invalid.

    Example:
        >>> render_heading(Heading(level=1, text="Hi"), {})
        '<h1>Hi</h1>'
    """
    ...
```

For simple functions, one line is fine:

```python
def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    ...
```

### Comments

**Use English for comments** (for international contributors):

```python
# ✅ Good — English
# Skip front matter if already parsed

# ❌ Avoid — Persian
# از front matter صرف‌نظر کن
```

**Explain WHY, not WHAT:**

```python
# ❌ Bad — obvious
# Increment i by 1
i += 1

# ✅ Good — explains reason
# Skip the blank line after front matter
i += 1
```

### Type Hints

Use type hints for all public functions:

```python
from typing import List, Optional, Dict, Any

def parse_text(text: str) -> Document:
    ...

def render_node(
    node: Node,
    doc: Optional[Document] = None,
    context: Optional[Dict[str, Any]] = None,
) -> str:
    ...
```

### Error Handling

Use custom exceptions from `errors.py`:

```python
from .errors import ParserError, RenderError

def parse_heading(line: str, line_num: int) -> Heading:
    if not line.startswith("#"):
        raise ParserError("Not a heading", line=line_num)
    ...
```

### Import Order

Standard library → third-party → local:

```python
# 1. Standard library
import os
import re
import json
from pathlib import Path
from typing import List, Dict

# 2. Third-party
from flask import Flask

# 3. Local
from .ast import Heading, Paragraph
from .errors import ParserError
```

### Code Organization

Order within a module:

1. Module docstring
2. Imports
3. Constants
4. Regex patterns
5. Classes
6. Public functions
7. Private functions (`_leading_underscore`)
8. `if __name__ == "__main__":`

---

## 7. Writing Tests

### Test Structure

Tests live in `tests/`. Each test file mirrors a source file:

```
src/markup_plus/parser.py    →  tests/test_parser.py
src/markup_plus/renderer.py  →  tests/test_renderer.py
```

### Test Naming

```python
# Pattern: test_<what>_<expected_behavior>

def test_heading_parses():
    """Heading with # parses to Heading node."""

def test_heading_renders_with_id():
    """Heading renders with slug as id attribute."""

def test_heading_ignores_leading_whitespace():
    """Heading works with leading spaces."""
```

### Test Anatomy (AAA Pattern)

```python
def test_variable_substitution():
    # Arrange — setup
    source = "@let name = \"Ali\"\n\nHello {name}!"
    
    # Act — execute
    html = to_html(source)
    
    # Assert — verify
    assert "Hello Ali!" in html
    assert "{name}" not in html
```

### Testing Parser

```python
from markup_plus.parser import parse_text
from markup_plus.ast import Heading, Paragraph


def test_parse_heading():
    doc = parse_text("# Hello")
    assert len(doc.children) == 1
    assert isinstance(doc.children[0], Heading)
    assert doc.children[0].level == 1
    assert doc.children[0].text == "Hello"


def test_parse_h1_to_h6():
    for level in range(1, 7):
        source = "#" * level + " Title"
        doc = parse_text(source)
        assert doc.children[0].level == level
```

### Testing Renderer

```python
from markup_plus.renderer import to_html


def test_render_bold():
    html = to_html("**bold**")
    assert "<strong>bold</strong>" in html


def test_render_chart():
    source = """
@chart(type="bar")
data: [1, 2, 3]
labels: ["A", "B", "C"]
@end
"""
    html = to_html(source)
    assert 'class="chart-block"' in html
    assert "mup-chart" in html
```

### Testing CLI

```python
import subprocess
import tempfile
from pathlib import Path


def test_cli_converts_file():
    with tempfile.TemporaryDirectory() as tmp:
        input_file = Path(tmp) / "test.mup"
        input_file.write_text("# Hello\n")
        
        result = subprocess.run(
            ["mup", str(input_file)],
            capture_output=True,
            text=True,
        )
        
        assert result.returncode == 0
        output_file = input_file.with_suffix(".html")
        assert output_file.exists()
        assert "<h1" in output_file.read_text()
```

### Testing Errors

```python
import pytest
from markup_plus.errors import ParserError


def test_invalid_directive_raises():
    with pytest.raises(ParserError):
        parse_text("@unknown_directive")
```

### Test Coverage

Aim for **80%+ coverage**. Check with:

```bash
pytest tests/ --cov=src/markup_plus --cov-report=term-missing
```

### What to Test

**Always test:**

- ✅ New features
- ✅ Bug fixes (regression test)
- ✅ Edge cases (empty input, unicode, large files)
- ✅ Error handling

**Don't worry about:**

- ❌ Third-party libraries (they test themselves)
- ❌ Simple getters/setters
- ❌ Every branch of every function

### Skip vs. Xfail

```python
import pytest


@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_broken():
    assert False
```

---

## 8. Writing Documentation

### Which File to Update?

| Change | Update |
|--------|--------|
| New feature | `GUIDE.md` + `CHANGELOG.md` |
| Bug fix | `CHANGELOG.md` |
| Architecture change | `DEVELOPER.md` |
| New example | `examples/` + maybe `TUTORIAL.md` |
| CLI change | `GUIDE.md` section 8 |
| API change | `DEVELOPER.md` + `GUIDE.md` |

### Documentation Style

**Use clear, active voice:**

```markdown
❌ The file is converted by running mup.
✅ Run `mup` to convert the file.
```

**Provide examples for everything:**

````markdown
To create a note:

```mup
@note
This is a note.
@end
```

Show input AND output:

Input	Output
**bold**	bold
*italic*	italic
Use tables for reference:

Option	Type	Default
width	number	auto
Markdown Conventions
Use # for H1 (only one per file)

Use ## for H2 (sections)

Use ### for H3 (subsections)

Blank line before/after headings

Blank line before/after code blocks

Use fenced code blocks (```) not indented

Specify language for code blocks: ```python

Code Examples in Docs
Always specify the language:

markdown
```python
def hello():
    print("Hi")
```
For Markup+ syntax:

markdown
```mup
# Hello

@note
Note text.
@end
```
For shell commands:

markdown
```bash
mup file.mup
```
9. Commit Message Guidelines
We follow Conventional Commits: https://www.conventionalcommits.org/

Format
text
<type>(<scope>): <subject>

<body>

<footer>
Types
Type	Use For
feat	New feature
fix	Bug fix
docs	Documentation only
test	Adding tests
refactor	Code refactoring (no behavior change)
perf	Performance improvement
style	Formatting (no code change)
chore	Maintenance
ci	CI/CD changes
build	Build system changes
Scopes (Optional)
parser — parser.py changes

renderer — renderer.py changes

lexer — lexer.py changes

ast — ast.py changes

cli — CLI changes

docs — documentation

Examples
Simple:

text
feat: add @run directive for code blocks
fix: correct RTL detection for mixed text
docs: add examples to GUIDE.md
test: add parser tests for nested lists
With scope:

text
feat(parser): support @import with relative paths
fix(renderer): escape HTML in code blocks
docs(cli): document --debug flag
With body:

text
feat(parser): add @import directive

Allow splitting large documents into multiple files.

- Resolve paths relative to importing file
- Detect and prevent circular imports
- Show friendly error for missing files

Closes #42
Breaking change:

text
feat(api)!: change to_html signature

BREAKING CHANGE: `to_html()` now requires `base_dir` parameter
for resolving @import paths.

Migration: pass `base_dir=os.getcwd()` for old behavior.
Rules
✅ Do:

Use imperative mood: "add" not "added"

Lowercase first letter

No period at end

Max 72 characters in subject

Wrap body at 72 characters

Reference issues: Closes #42, Fixes #100

❌ Don't:

"Fixed bug" (not descriptive)

"Update" (too vague)

"WIP" (don't commit WIP)

Emojis in commits (they're in PR titles)

10. Pull Request Process
Before Submitting
Checklist:

□ My code follows the style guide
□ I ran black src/ tests/
□ I ran ruff check src/ tests/
□ I ran pytest tests/ -v and all pass
□ I added tests for new functionality
□ I updated documentation
□ I updated CHANGELOG.md
□ My commits follow the commit guidelines
□ My branch is up to date with upstream/master
PR Title
Follow the same format as commits:

text
feat: add @run directive for code blocks
fix: correct RTL detection
docs: improve CLI reference
PR Description Template
markdown
## What does this PR do?

Brief description of changes.

## Why is this needed?

Link to issue or explain motivation.

## How was this tested?

- Test 1: description
- Test 2: description

## Screenshots (if UI change)

Before | After
-------|------
![]()  | ![]()

## Checklist

- [x] Tests added/updated
- [x] Docs updated
- [x] CHANGELOG updated
- [x] No breaking changes
- [ ] Breaking changes (explain below)

## Related Issues

Closes #42
Review Process
Automated checks — CI runs tests, linting

Maintainer review — usually within 1-3 days

Feedback — you may be asked to change things

Approval — once approved, maintainer merges

Responding to Feedback
Be patient — maintainers are volunteers

Be open — feedback improves the code

Ask questions — if unclear, ask

Don't take it personally — it's about the code

After Merge
Delete your branch (GitHub does this automatically)

Sync your fork:

bash
git checkout master
git fetch upstream
git merge upstream/master
git push origin master
Your contribution will be in the next release! 🎉

If Your PR is Stale
If it's been a while:

Rebase on latest master:

bash
git fetch upstream
git rebase upstream/master
git push --force-with-lease origin your-branch
Leave a comment asking for review

If no response in 2 weeks, ping again

11. Reporting Bugs
Before Reporting
Search existing issues — might already be reported

Update to latest version — might be fixed

Try minimal reproduction — isolate the problem

Bug Report Template
markdown
**Describe the bug**

A clear description of what's wrong.

**To Reproduce**

Steps:
1. Create file `test.mup` with content:
   ```mup
   @let name = "Ali"
   
   Hello {name}!
Run mup test.mup

Open test.html

See error: {name} not replaced

Expected behavior

Should display Hello Ali!.

Actual behavior

Displays Hello {name}! — variable not substituted.

Environment

OS: Windows 10

Python: 3.11.5

Markup+: 0.6.0 (output of mup --version)

Additional context

Screenshot attached. Also happens with other variables.

text

### Good Bug Reports

✅ **Include:**
- Minimal reproduction (smallest possible file)
- Exact commands run
- Full error message (copy-paste, not screenshot)
- Environment details
- What you expected vs what happened

❌ **Avoid:**
- "It doesn't work"
- Huge files (isolate the problem)
- Screenshots of text (copy-paste text)
- "Fix this now" (be patient)

---

## 12. Suggesting Features

### Before Suggesting

1. **Check the roadmap** — might be planned
2. **Search existing discussions** — might already exist
3. **Consider scope** — is it useful for many users?

### Feature Request Template

```markdown
**Is your feature request related to a problem?**

Yes — I'm always frustrated when I have to...

**Describe the solution you'd like**

I want a `@video` directive that...

Example syntax:
```mup
@video(url="https://youtube.com/watch?v=...")
@end
Describe alternatives you've considered

I could embed with HTML iframe, but that's ugly.

Additional context

Useful for blog posts with embedded videos.

text

### Feature Discussion

For big features, we'll discuss:

- **Scope** — what's in / out
- **Syntax** — how users write it
- **Implementation** — technical approach
- **Breaking changes** — if any
- **Timeline** — which version

---

## 13. Translation Guide

### Translating Documentation

Currently, documentation is in English. To add translations:

1. Create a `docs/` subfolder for your language:
docs/
├── en/
│ ├── GUIDE.md
│ ├── TUTORIAL.md
│ └── DEVELOPER.md
├── fa/ ← Persian
│ ├── GUIDE.md
│ └── ...
└── ar/ ← Arabic

text

2. Translate the files
3. Update the language switcher (if any)
4. Submit a PR

### Translating CLI Messages

CLI messages are in `src/markup_plus/cli/`:

- `theme.py` — colors (no translation needed)
- `display.py` — user messages
- `errors.py` — error messages
- `commands.py` — command descriptions

To add i18n:

1. Create `src/markup_plus/i18n/` folder
2. Add message catalogs:
i18n/
├── en.json
├── fa.json
└── ar.json

text

3. Update CLI to load based on locale

*(This is a future feature — see roadmap.)*

### Translation Guidelines

- **Be accurate** — don't just Google Translate
- **Keep technical terms** — "parser" stays "parser"
- **Match tone** — formal/informal consistent
- **Update code examples** — but keep syntax the same
- **Test rendered output** — make sure it displays correctly

---

## 14. Recognition

### Contributors

All contributors are listed in:

- `CONTRIBUTORS.md` (if exists)
- GitHub's automatic contributor list
- Release notes for their contributions

### Special Thanks

Top contributors get:

- 🏆 Mention in release notes
- ⭐ Featured in README
- 🎁 Markup+ swag (if available)

### Hall of Fame

Significant contributions recognized in:

- `CHANGELOG.md` — with name
- GitHub Releases — with thanks
- Project website (when available)

---

## 📚 Quick Reference

### Common Commands

```bash
# Setup
git clone https://github.com/YOUR-USERNAME/markup-plus.git
cd markup-plus
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -e .
pip install pytest pytest-cov black ruff

# Daily workflow
git checkout master
git pull upstream master
git checkout -b feature/my-feature
# ... make changes ...
black src/ tests/
ruff check src/ tests/ --fix
pytest tests/ -v
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature

# Update from upstream
git fetch upstream
git rebase upstream/master

# Check test coverage
pytest tests/ --cov=src/markup_plus --cov-report=html
# Open htmlcov/index.html in browser
Useful Links
Repository: https://github.com/USERNAME/markup-plus

Issues: https://github.com/USERNAME/markup-plus/issues

Discussions: https://github.com/USERNAME/markup-plus/discussions

User Guide: GUIDE.md

Developer Guide: DEVELOPER.md

Tutorial: TUTORIAL.md

Changelog: CHANGELOG.md

Getting Help
Stuck? Ask:

💬 GitHub Discussions — for questions

🐛 GitHub Issues — for bugs

📧 Email maintainer — for private concerns

🙏 Thank You
Every contribution — no matter how small — makes Markup+ better.

Whether you fixed a typo, reported a bug, added a feature, or just told a
friend about us — thank you!

Happy coding! 💜

Last updated: January 2025
Version: 0.6.0
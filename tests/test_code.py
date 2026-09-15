"""Tests for code block parsing and rendering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import CodeBlock
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Basic parsing
# ============================================================

def test_simple_code_block():
    doc = parse_text("```\nhello\n```")
    node = doc.children[0]
    assert isinstance(node, CodeBlock)
    assert node.language == ""
    assert node.code == "hello"


def test_code_block_with_language():
    doc = parse_text("```python\nprint('hi')\n```")
    node = doc.children[0]
    assert node.language == "python"
    assert node.code == "print('hi')"


def test_multiline_code_block():
    src = "```python\ndef foo():\n    return 42\n```"
    node = parse_text(src).children[0]
    assert node.code == "def foo():\n    return 42"


def test_code_block_preserves_blank_lines():
    src = "```\nline1\n\nline3\n```"
    node = parse_text(src).children[0]
    assert node.code == "line1\n\nline3"


# ============================================================
# Options parsing
# ============================================================

def test_code_block_with_title_option():
    src = '```python {title="app.py"}\nprint("hi")\n```'
    node = parse_text(src).children[0]
    assert node.title == "app.py"


def test_code_block_defaults():
    src = "```python\ncode\n```"
    node = parse_text(src).children[0]
    assert node.copy is True
    assert node.download is True
    assert node.run is False
    assert node.linenos is False


def test_code_block_disable_copy():
    src = "```python {copy=false}\ncode\n```"
    node = parse_text(src).children[0]
    assert node.copy is False


def test_code_block_disable_download():
    src = "```python {download=false}\ncode\n```"
    node = parse_text(src).children[0]
    assert node.download is False


def test_code_block_linenos_option():
    src = "```python {linenos}\ncode\n```"
    node = parse_text(src).children[0]
    assert node.linenos is True


def test_code_block_highlight_option():
    src = "```python {hl=[2,4]}\ncode\n```"
    node = parse_text(src).children[0]
    assert node.highlight == [2, 4]


def test_code_block_wrap_option():
    src = "```python {wrap}\ncode\n```"
    node = parse_text(src).children[0]
    assert node.wrap is True


# ============================================================
# Rendering — basic
# ============================================================

def test_render_code_block():
    html = to_html("```\nhello\n```")
    assert "<pre>" in html
    assert "hello" in html
    assert "</pre>" in html


def test_render_code_block_with_language_class():
    html = to_html("```python\nprint('hi')\n```")
    assert 'class="language-python"' in html


def test_render_code_block_with_title():
    html = to_html('```python {title="app.py"}\nprint("hi")\n```')
    assert "app.py" in html
    assert 'class="code-title"' in html


# ============================================================
# Rendering — buttons (data-action based, not function names)
# ============================================================

def test_render_code_block_has_copy_button():
    html = to_html("```python\ncode\n```")
    assert 'data-action="copy"' in html
    assert "Copy" in html


def test_render_code_block_has_download_button():
    html = to_html("```python\ncode\n```")
    assert 'data-action="download"' in html
    assert "Download" in html


def test_render_code_block_no_copy_when_disabled():
    html = to_html("```python {copy=false}\ncode\n```")
    assert 'data-action="copy"' not in html


def test_render_code_block_no_download_when_disabled():
    html = to_html("```python {download=false}\ncode\n```")
    assert 'data-action="download"' not in html


def test_render_code_block_no_buttons_when_both_disabled():
    html = to_html("```python {copy=false download=false}\ncode\n```")
    assert 'data-action="copy"' not in html
    assert 'data-action="download"' not in html


# ============================================================
# Rendering — preview button (for HTML/CSS/JS)
# ============================================================

def test_render_code_block_has_preview_for_html():
    html = to_html("```html\n<p>hi</p>\n```")
    assert 'data-action="preview"' in html
    assert "Preview" in html


def test_render_code_block_has_preview_for_css():
    html = to_html("```css\nbody { color: red; }\n```")
    assert 'data-action="preview"' in html


def test_render_code_block_has_preview_for_javascript():
    html = to_html("```javascript\nconsole.log('hi');\n```")
    assert 'data-action="preview"' in html


def test_render_code_block_no_preview_for_python():
    html = to_html("```python\nprint('hi')\n```")
    assert 'data-action="preview"' not in html


# ============================================================
# Rendering — line numbers (no longer rendered, but code should appear)
# ============================================================

def test_render_code_block_with_linenos():
    """Line numbers option is parsed, but code is rendered cleanly."""
    html = to_html("```python {linenos}\ncode\n```")
    assert "<pre>" in html
    assert "code" in html


def test_render_code_block_with_highlight():
    """Highlight option is parsed, and content appears."""
    src = "```python {linenos hl=[2]}\nline1\nline2\nline3\n```"
    html = to_html(src)
    assert "line1" in html
    assert "line2" in html
    assert "line3" in html


# ============================================================
# Security — HTML escaping inside code blocks
# ============================================================

def test_code_block_escapes_html():
    html = to_html("```\n<script>alert(1)</script>\n```")
    # The raw <script> should be escaped inside <pre><code>
    assert "&lt;script&gt;" in html
    # Extract code body and ensure the raw script isn't there
    start = html.find('<pre><code')
    if start != -1:
        end = html.find('</code></pre>', start)
        code_section = html[start:end]
        assert "<script>alert" not in code_section
        assert "&lt;script&gt;alert" in code_section


def test_inline_code_not_confused_with_block():
    html = to_html("This is `inline` code.")
    assert "<p" in html
    assert "<code>inline</code>" in html


# ============================================================
# NEW: Links and strikethrough
# ============================================================

def test_simple_link():
    html = to_html("Visit [Google](https://google.com) now.")
    assert '<a href="https://google.com"' in html
    assert ">Google</a>" in html


def test_link_with_title():
    html = to_html('[Google](https://google.com "Search")')
    assert 'title="Search"' in html


def test_autolink():
    html = to_html("Visit <https://example.com> for more.")
    assert '<a href="https://example.com"' in html


def test_strikethrough():
    html = to_html("This is ~~old~~ new.")
    assert "<del>old</del>" in html
"""Tests for the Markup+ renderer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.renderer import render_inline, to_html


def test_bold():
    assert render_inline("**bold**") == "<strong>bold</strong>"


def test_italic():
    assert render_inline("*italic*") == "<em>italic</em>"


def test_inline_code():
    assert render_inline("`code`") == "<code>code</code>"


def test_html_escape():
    assert render_inline("<script>") == "&lt;script&gt;"


def test_heading_to_html():
    html = to_html("# Hello", title="Test")
    assert "<h1>Hello</h1>" in html
    assert "<title>Test</title>" in html


def test_paragraph_to_html():
    html = to_html("Some text.")
    assert "<p>Some text.</p>" in html
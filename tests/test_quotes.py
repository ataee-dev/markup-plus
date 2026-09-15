"""Tests for blockquotes and horizontal rules."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import BlockQuote, HorizontalRule
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Blockquote tests
# ============================================================

def test_simple_blockquote():
    doc = parse_text("> Hello")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, BlockQuote)
    assert node.text == "Hello"


def test_multiline_blockquote():
    doc = parse_text("> Line 1\n> Line 2\n> Line 3")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert node.text == "Line 1\nLine 2\nLine 3"


def test_render_blockquote():
    html = to_html("> Hello world")
    assert "<blockquote>" in html
    assert "<p>Hello world</p>" in html
    assert "</blockquote>" in html


def test_render_blockquote_with_formatting():
    html = to_html("> This is **bold**")
    assert "<strong>bold</strong>" in html


# ============================================================
# Horizontal rule tests
# ============================================================

def test_hr_dashes():
    doc = parse_text("---")
    assert len(doc.children) == 1
    assert isinstance(doc.children[0], HorizontalRule)


def test_hr_asterisks():
    doc = parse_text("***")
    assert len(doc.children) == 1
    assert isinstance(doc.children[0], HorizontalRule)


def test_hr_underscores():
    doc = parse_text("___")
    assert len(doc.children) == 1
    assert isinstance(doc.children[0], HorizontalRule)


def test_hr_longer():
    doc = parse_text("-----")
    assert isinstance(doc.children[0], HorizontalRule)


def test_render_hr():
    html = to_html("---")
    assert "<hr>" in html
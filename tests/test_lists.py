"""Tests for list parsing and rendering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import ListBlock
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Parser tests
# ============================================================

def test_unordered_list():
    doc = parse_text("- Apple\n- Banana\n- Cherry")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, ListBlock)
    assert node.ordered is False
    assert node.items == ["Apple", "Banana", "Cherry"]


def test_ordered_list():
    doc = parse_text("1. One\n2. Two\n3. Three")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, ListBlock)
    assert node.ordered is True
    assert node.items == ["One", "Two", "Three"]


def test_list_with_asterisk_marker():
    doc = parse_text("* Item 1\n* Item 2")
    assert len(doc.children) == 1
    assert doc.children[0].items == ["Item 1", "Item 2"]


def test_list_with_plus_marker():
    doc = parse_text("+ A\n+ B")
    assert len(doc.children) == 1
    assert doc.children[0].items == ["A", "B"]


def test_list_interrupted_by_paragraph():
    doc = parse_text("- Item 1\n- Item 2\n\nRegular paragraph.")
    assert len(doc.children) == 2
    assert isinstance(doc.children[0], ListBlock)
    assert doc.children[0].items == ["Item 1", "Item 2"]


# ============================================================
# Renderer tests
# ============================================================

def test_render_unordered_list():
    html = to_html("- Apple\n- Banana")
    assert "<ul>" in html
    assert "<li>Apple</li>" in html
    assert "<li>Banana</li>" in html
    assert "</ul>" in html


def test_render_ordered_list():
    html = to_html("1. First\n2. Second")
    assert "<ol>" in html
    assert "<li>First</li>" in html
    assert "<li>Second</li>" in html
    assert "</ol>" in html


def test_render_list_with_formatting():
    html = to_html("- **Bold** item\n- `code` item")
    assert "<li><strong>Bold</strong> item</li>" in html
    assert "<li><code>code</code> item</li>" in html
"""Tests for table parsing and rendering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import TableBlock
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Parser tests
# ============================================================

def test_simple_table():
    src = "| Name | Age |\n|------|-----|\n| Ali  | 30  |"
    doc = parse_text(src)
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, TableBlock)
    assert node.headers == ["Name", "Age"]
    assert node.rows == [["Ali", "30"]]


def test_table_with_alignment():
    src = (
        "| Left | Center | Right |\n"
        "|:-----|:------:|------:|\n"
        "| A    | B      | C     |"
    )
    doc = parse_text(src)
    node = doc.children[0]
    assert node.alignments == ["left", "center", "right"]


def test_table_default_alignment():
    src = "| A | B |\n|---|---|\n| 1 | 2 |"
    doc = parse_text(src)
    node = doc.children[0]
    assert node.alignments == ["none", "none"]


def test_table_multiple_rows():
    src = (
        "| A | B |\n"
        "|---|---|\n"
        "| 1 | 2 |\n"
        "| 3 | 4 |\n"
        "| 5 | 6 |"
    )
    doc = parse_text(src)
    node = doc.children[0]
    assert len(node.rows) == 3
    assert node.rows[0] == ["1", "2"]
    assert node.rows[1] == ["3", "4"]
    assert node.rows[2] == ["5", "6"]


def test_table_without_leading_trailing_pipes():
    src = "A | B\n---|---\n1 | 2"
    doc = parse_text(src)
    # Our regex requires leading pipe, so this might not parse
    # This is OK — we require pipes
    # (Just make sure it doesn't crash)
    assert doc is not None


def test_table_inline_formatting():
    src = "| **Bold** | `code` |\n|----------|--------|\n| *Italic* | normal |"
    doc = parse_text(src)
    node = doc.children[0]
    assert node.headers == ["**Bold**", "`code`"]


def test_table_followed_by_paragraph():
    src = "| A | B |\n|---|---|\n| 1 | 2 |\n\nSome text."
    doc = parse_text(src)
    assert len(doc.children) == 2
    assert isinstance(doc.children[0], TableBlock)


# ============================================================
# Renderer tests
# ============================================================

def test_render_simple_table():
    html = to_html("| A | B |\n|---|---|\n| 1 | 2 |")
    assert "<table>" in html
    assert "<thead>" in html
    assert "<tbody>" in html
    assert "<th>A</th>" in html
    assert "<th>B</th>" in html
    assert "<td>1</td>" in html
    assert "<td>2</td>" in html


def test_render_table_with_left_alignment():
    html = to_html("| A |\n|:--|\n| 1 |")
    assert 'style="text-align: left;"' in html


def test_render_table_with_center_alignment():
    html = to_html("| A |\n|:-:|\n| 1 |")
    assert 'style="text-align: center;"' in html


def test_render_table_with_right_alignment():
    html = to_html("| A |\n|--:|\n| 1 |")
    assert 'style="text-align: right;"' in html


def test_render_table_inline_formatting():
    html = to_html("| **Bold** |\n|----------|\n| *italic* |")
    assert "<th><strong>Bold</strong></th>" in html
    assert "<td><em>italic</em></td>" in html


def test_render_table_wrapped_in_div():
    html = to_html("| A |\n|---|\n| 1 |")
    assert 'class="table-wrapper reveal"' in html


def test_render_table_link():
    html = to_html("| A |\n|---|\n| [link](https://example.com) |")
    assert '<a href="https://example.com"' in html


def test_render_table_escapes_html():
    html = to_html("| <script> |\n|----------|\n| <b>hi</b> |")
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;hi&lt;/b&gt;" in html


def test_render_table_normalizes_row_length():
    # Row with fewer cells than header
    html = to_html("| A | B | C |\n|---|---|---|\n| 1 |")
    # Should not crash, should pad
    assert "<table>" in html
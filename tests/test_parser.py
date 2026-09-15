"""Tests for the Markup+ parser."""

import sys
from pathlib import Path

# Add src to path for direct test runs
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import Document, Heading, Paragraph
from markup_plus.parser import parse_text


def test_empty_document():
    doc = parse_text("")
    assert isinstance(doc, Document)
    assert doc.children == []


def test_single_heading():
    doc = parse_text("# Hello")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, Heading)
    assert node.level == 1
    assert node.text == "Hello"


def test_h2_h3():
    doc = parse_text("## Level 2\n### Level 3")
    assert len(doc.children) == 2
    assert doc.children[0].level == 2
    assert doc.children[1].level == 3


def test_paragraph():
    doc = parse_text("Just some text.")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, Paragraph)
    assert node.text == "Just some text."


def test_mixed():
    src = "# Title\n\nSome text.\n\n## Subtitle\n"
    doc = parse_text(src)
    assert len(doc.children) == 3
    assert isinstance(doc.children[0], Heading)
    assert isinstance(doc.children[1], Paragraph)
    assert isinstance(doc.children[2], Heading)
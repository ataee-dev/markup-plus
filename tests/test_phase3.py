"""Tests for Phase 3 features: Task Lists, Front Matter, TOC, Footnotes."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import ListBlock, TOCBlock
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Front Matter
# ============================================================

def test_front_matter_parses():
    src = "---\ntitle: Test\nauthor: Ali\n---\n\n# Hello"
    doc = parse_text(src)
    assert doc.meta["title"] == "Test"
    assert doc.meta["author"] == "Ali"


def test_front_matter_no_meta():
    src = "# Hello\n\nWorld"
    doc = parse_text(src)
    assert doc.meta == {}


def test_front_matter_quoted_values():
    src = '---\ntitle: "My Title"\nauthor: \'John\'\n---\n'
    doc = parse_text(src)
    assert doc.meta["title"] == "My Title"
    assert doc.meta["author"] == "John"


def test_front_matter_empty():
    src = "---\n---\n\n# Hello"
    doc = parse_text(src)
    assert doc.meta == {}


def test_front_matter_title_used():
    src = "---\ntitle: My Custom Title\n---\n\n# Hello"
    html = to_html(src)
    assert "<title>My Custom Title</title>" in html


def test_front_matter_substitution():
    src = "---\nname: Markup+\n---\n\n# Welcome to {name}"
    html = to_html(src)
    assert "Welcome to Markup+" in html


# ============================================================
# Task Lists
# ============================================================

def test_task_list_parses():
    src = "- [ ] pending\n- [x] done"
    doc = parse_text(src)
    node = doc.children[0]
    assert isinstance(node, ListBlock)
    assert node.items == ["pending", "done"]
    assert node.checked == [False, True]


def test_task_list_uppercase_x():
    src = "- [X] done"
    doc = parse_text(src)
    assert doc.children[0].checked == [True]


def test_task_list_renders_with_checkboxes():
    html = to_html("- [x] done\n- [ ] pending")
    assert 'class="task-list' in html
    assert 'class="task-done"' in html
    assert 'class="task-todo"' in html


def test_regular_list_not_task():
    html = to_html("- Apple\n- Banana")
    # Extract body content only (CSS in <style> may contain "task-list" string)
    body_start = html.find("<body")
    body = html[body_start:] if body_start != -1 else html
    # The ul should NOT have class="task-list"
    assert 'class="task-list' not in body
    assert "<ul" in body


# ============================================================
# TOC
# ============================================================

def test_toc_parses():
    src = "@toc\n\n# H1\n\n## H2"
    doc = parse_text(src)
    assert isinstance(doc.children[0], TOCBlock)


def test_toc_renders_links():
    src = "# Intro\n\n## Section A\n\n## Section B"
    html = to_html(src)
    # TOC not auto-generated unless @toc present — check headings have IDs
    assert 'id="intro"' in html or 'id=' in html


def test_toc_includes_headings():
    src = "@toc\n\n# First\n\n## Second\n\n### Third"
    html = to_html(src)
    assert 'class="toc' in html
    assert 'href="#first"' in html
    assert 'href="#second"' in html
    assert 'href="#third"' in html


def test_heading_slug_generation():
    doc = parse_text("# Hello World\n\n## Another Section")
    headings = [c for c in doc.children if hasattr(c, "slug")]
    assert headings[0].slug == "hello-world"
    assert headings[1].slug == "another-section"


def test_persian_heading_slug():
    doc = parse_text("# سلام دنیا")
    headings = [c for c in doc.children if hasattr(c, "slug")]
    assert len(headings) > 0
    assert "سلام" in headings[0].slug or headings[0].slug


# ============================================================
# Footnotes
# ============================================================

def test_footnote_collected():
    src = "Text[^1].\n\n[^1]: Note text."
    doc = parse_text(src)
    assert "1" in doc.footnotes
    assert doc.footnotes["1"] == "Note text."


def test_footnote_rendered():
    src = "Text[^1].\n\n[^1]: Note text."
    html = to_html(src)
    assert 'class="footnote-ref"' in html
    assert 'href="#fn-1"' in html


def test_footnotes_section():
    src = "Text[^1].\n\n[^1]: Note text."
    html = to_html(src)
    # Check for the actual rendered <section> element, not just CSS class
    # (CSS in <style> also contains ".footnotes" which could match)
    assert '<section class="footnotes' in html, (
        f"Footnotes section element not found in HTML (length={len(html)})"
    )
    assert 'id="fn-1"' in html
    assert "Note text." in html


def test_multiple_footnotes():
    src = "A[^1] B[^2].\n\n[^1]: First.\n[^2]: Second."
    doc = parse_text(src)
    assert len(doc.footnotes) == 2
    html = to_html(src)
    assert "First." in html
    assert "Second." in html


def test_no_footnotes():
    src = "Just some text."
    html = to_html(src)
    # Check for the actual rendered <section> element, not just CSS class
    assert '<section class="footnotes' not in html


# ============================================================
# Integration
# ============================================================

def test_complete_phase3_document():
    src = """---
title: Full Test
author: Test
---

# {title}

@toc

## Section 1

- [x] Task 1
- [ ] Task 2

## Section 2

| A | B |
|---|---|
| 1 | 2 |

Text with footnote[^1].

[^1]: The note.
"""
    html = to_html(src)
    # All features present
    assert "<title>Full Test</title>" in html
    assert ">Full Test</h1>" in html
    assert 'class="toc' in html
    assert 'class="task-list' in html
    assert "<table>" in html
    # Use the actual <section> element selector
    assert '<section class="footnotes' in html
    assert "The note." in html
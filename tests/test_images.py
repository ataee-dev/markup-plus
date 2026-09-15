"""Tests for image parsing and rendering."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from markup_plus.ast import ImageBlock
from markup_plus.parser import parse_text
from markup_plus.renderer import to_html


# ============================================================
# Parser tests
# ============================================================

def test_simple_image():
    doc = parse_text("![alt](url.png)")
    assert len(doc.children) == 1
    node = doc.children[0]
    assert isinstance(node, ImageBlock)
    assert node.alt == "alt"
    assert node.url == "url.png"
    assert node.title == ""


def test_image_with_title():
    doc = parse_text('![alt](url.png "Title")')
    node = doc.children[0]
    assert node.alt == "alt"
    assert node.url == "url.png"
    assert node.title == "Title"


def test_image_with_width():
    doc = parse_text("![alt](url.png){width=400}")
    node = doc.children[0]
    assert node.width == "400"


def test_image_with_height():
    doc = parse_text("![alt](url.png){height=300}")
    node = doc.children[0]
    assert node.height == "300"


def test_image_with_align():
    doc = parse_text("![alt](url.png){align=center}")
    node = doc.children[0]
    assert node.align == "center"


def test_image_with_caption():
    doc = parse_text('![alt](url.png){caption="A nice photo"}')
    node = doc.children[0]
    assert node.caption == "A nice photo"


def test_image_with_link():
    doc = parse_text("![alt](url.png){link=https://example.com}")
    node = doc.children[0]
    assert node.link == "https://example.com"


def test_image_with_multiple_options():
    doc = parse_text('![alt](url.png){width=400 align=center caption="Nice"}')
    node = doc.children[0]
    assert node.width == "400"
    assert node.align == "center"
    assert node.caption == "Nice"


def test_image_empty_alt():
    doc = parse_text("![](url.png)")
    node = doc.children[0]
    assert isinstance(node, ImageBlock)
    assert node.alt == ""
    assert node.url == "url.png"


def test_image_with_url_query():
    doc = parse_text("![alt](https://example.com/img.png?v=1)")
    node = doc.children[0]
    assert node.url == "https://example.com/img.png?v=1"


# ============================================================
# Renderer tests
# ============================================================

def test_render_simple_image():
    html = to_html("![alt](url.png)")
    assert "<img" in html
    assert 'src="url.png"' in html
    assert 'alt="alt"' in html


def test_render_image_with_title():
    html = to_html('![alt](url.png "Title")')
    assert 'title="Title"' in html


def test_render_image_with_width():
    html = to_html("![alt](url.png){width=400}")
    assert 'width="400"' in html


def test_render_image_with_height():
    html = to_html("![alt](url.png){height=300}")
    assert 'height="300"' in html


def test_render_image_centered():
    html = to_html("![alt](url.png){align=center}")
    assert 'image-align-center' in html


def test_render_image_left_aligned():
    html = to_html("![alt](url.png){align=left}")
    assert 'image-align-left' in html


def test_render_image_right_aligned():
    html = to_html("![alt](url.png){align=right}")
    assert 'image-align-right' in html


def test_render_image_with_caption():
    html = to_html('![alt](url.png){caption="Nice"}')
    assert "<figure" in html
    assert "Nice</figcaption>" in html


def test_render_image_with_link():
    html = to_html("![alt](url.png){link=https://example.com}")
    assert '<a href="https://example.com"' in html
    assert 'target="_blank"' in html
    assert 'rel="noopener noreferrer"' in html


def test_render_image_with_caption_formatting():
    html = to_html('![alt](url.png){caption="A **bold** caption"}')
    assert "A <strong>bold</strong> caption</figcaption>" in html


def test_render_image_full_featured():
    src = '![alt](url.png){width=400 align=center caption="Nice" link=https://example.com}'
    html = to_html(src)
    assert 'image-align-center' in html
    assert '<a href="https://example.com"' in html
    assert "Nice</figcaption>" in html
    assert 'width="400"' in html


# ============================================================
# Security
# ============================================================

def test_render_image_escapes_alt_html():
    html = to_html('![<script>alert(1)</script>](url.png)')
    assert 'alt="&lt;script&gt;alert(1)&lt;/script&gt;"' in html
    assert 'alt="<script>' not in html


def test_render_image_escapes_url_quotes():
    html = to_html('![alt](url.png)')
    assert 'src="url.png"' in html


def test_render_image_escapes_ampersand_in_url():
    html = to_html('![alt](url.png?a=1&b=2)')
    assert 'src="url.png?a=1&amp;b=2"' in html


def test_render_image_simple_title_works():
    html = to_html('![alt](url.png "Simple Title")')
    assert "<img" in html
    assert 'title="Simple Title"' in html


def test_render_image_title_with_ampersand():
    html = to_html('![alt](url.png "Tom & Jerry")')
    assert "<img" in html
    assert 'title="Tom &amp; Jerry"' in html
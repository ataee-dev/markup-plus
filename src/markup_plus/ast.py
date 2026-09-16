"""
Markup+ Abstract Syntax Tree (AST)

Defines node types that represent the structure of a Markup+ document.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ============================================================
# Base
# ============================================================

@dataclass
class Node:
    """Base class for all AST nodes."""
    line: int = 0


# ============================================================
# Block-level nodes
# ============================================================

@dataclass
class Document(Node):
    """Root node — contains all blocks + metadata."""
    children: List[Node] = field(default_factory=list)
    meta: Dict[str, str] = field(default_factory=dict)
    footnotes: Dict[str, str] = field(default_factory=dict)


@dataclass
class Heading(Node):
    """# Heading 1, ## Heading 2, ### Heading 3"""
    level: int = 1
    text: str = ""
    slug: str = ""  # For TOC anchors


@dataclass
class Paragraph(Node):
    """Regular paragraph."""
    text: str = ""


@dataclass
class ListBlock(Node):
    """Ordered or unordered list. `checked` for task lists (True/False/None)."""
    ordered: bool = False
    items: List[str] = field(default_factory=list)
    checked: List = field(default_factory=list)


@dataclass
class BlockQuote(Node):
    """> Quoted text (can span multiple lines)"""
    text: str = ""


@dataclass
class HorizontalRule(Node):
    """--- separator"""
    pass


@dataclass
class CodeBlock(Node):
    """Fenced code block with advanced options."""
    language: str = ""
    code: str = ""
    title: str = ""
    copy: bool = True
    download: bool = True
    run: bool = False
    share: bool = False
    linenos: bool = False
    highlight: List[int] = field(default_factory=list)
    wrap: bool = False


@dataclass
class ImageBlock(Node):
    """![alt](url "title"){width=... align=... link=... caption=... desc=...}"""
    alt: str = ""
    url: str = ""
    title: str = ""
    width: str = ""
    height: str = ""
    align: str = ""
    link: str = ""
    caption: str = ""
    description: str = ""
    zoomable: bool = True


@dataclass
class GalleryBlock(Node):
    """@gallery {columns=N caption="..."} ... @end — a grid of images."""
    columns: int = 3
    images: List[ImageBlock] = field(default_factory=list)
    caption: str = ""


@dataclass
class TableBlock(Node):
    """| Header | Header |\n|--------|--------|\n| Cell   | Cell   |"""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    alignments: List[str] = field(default_factory=list)

@dataclass
class TOCBlock(Node):
    """@toc {title="..."} — auto-generated table of contents."""
    title: str = "Table of Contents"


@dataclass
class FootnoteRef(Node):
    """[^1] — inline footnote reference."""
    key: str = ""


# ============================================================
# Inline-level nodes (metadata only — parsed at render time)
# ============================================================

@dataclass
class Text(Node):
    """Plain text."""
    content: str = ""


@dataclass
class Bold(Node):
    """**bold**"""
    content: str = ""


@dataclass
class Italic(Node):
    """*italic*"""
    content: str = ""


@dataclass
class InlineCode(Node):
    """`code`"""
    content: str = ""


@dataclass
class Strikethrough(Node):
    """~~strikethrough~~"""
    content: str = ""


@dataclass
class Link(Node):
    """[text](url "title") — inline link"""
    text: str = ""
    url: str = ""
    title: str = ""


@dataclass
class AutoLink(Node):
    """<https://example.com>"""
    url: str = ""
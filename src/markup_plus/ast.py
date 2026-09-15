"""
Markup+ Abstract Syntax Tree (AST)

Defines node types that represent the structure of a Markup+ document.
"""

from dataclasses import dataclass, field
from typing import List


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
    """Root node — contains all blocks."""
    children: List[Node] = field(default_factory=list)


@dataclass
class Heading(Node):
    """# Heading 1, ## Heading 2, ### Heading 3"""
    level: int = 1
    text: str = ""


@dataclass
class Paragraph(Node):
    """Regular paragraph."""
    text: str = ""


@dataclass
class ListBlock(Node):
    """Ordered or unordered list."""
    ordered: bool = False
    items: List[str] = field(default_factory=list)


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
    """
    ![alt](url "title"){width=... align=... link=... caption=... desc=... zoomable=...}

    Attributes:
        alt:         Alt text
        url:         Image URL
        title:       HTML title attribute
        width:       Custom width (e.g. "400")
        height:      Custom height (e.g. "300")
        align:       Alignment: left, center, right
        link:        Wrap in <a> tag with this href
        caption:     Short caption displayed below image
        description: Longer description shown in lightbox
        zoomable:    Allow opening in lightbox (default True)
    """
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
    """
    @gallery {columns=N caption="..."} ... @end — a grid of images.

    Attributes:
        columns:  Number of columns (default 3)
        images:   List of ImageBlock items
        caption:  Gallery-level caption
    """
    columns: int = 3
    images: List[ImageBlock] = field(default_factory=list)
    caption: str = ""


# ============================================================
# Inline-level nodes
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
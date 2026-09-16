"""
Markup+ Abstract Syntax Tree (AST)

Defines node types that represent the structure of a Markup+ document.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


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
    """Root node — contains all blocks + metadata + variables."""
    children: List[Node] = field(default_factory=list)
    meta: Dict[str, str] = field(default_factory=dict)
    footnotes: Dict[str, str] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VariableDef(Node):
    """@let name = value"""
    name: str = ""
    value: Any = None
    raw_value: str = ""


@dataclass
class Heading(Node):
    """# Heading 1, ## Heading 2, ### Heading 3"""
    level: int = 1
    text: str = ""
    slug: str = ""


@dataclass
class Paragraph(Node):
    """Regular paragraph."""
    text: str = ""


@dataclass
class ListBlock(Node):
    """Ordered or unordered list. `checked` for task lists."""
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
    """![alt](url "title"){options}"""
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
    """@gallery {columns=N} ... @end"""
    columns: int = 3
    images: List[ImageBlock] = field(default_factory=list)
    caption: str = ""


@dataclass
class TableBlock(Node):
    """| Header | Header |"""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    alignments: List[str] = field(default_factory=list)


@dataclass
class TOCBlock(Node):
    """@toc {title="..."}"""
    title: str = "Table of Contents"


# ============================================================
# Control flow nodes (Phase 4)
# ============================================================

@dataclass
class IfBlock(Node):
    """@if ... @elif ... @else ... @endif"""
    branches: List = field(default_factory=list)


@dataclass
class EachBlock(Node):
    """@each item in items ... @end"""
    item_name: str = ""
    index_name: str = ""
    iterable_expr: str = ""
    children: List[Node] = field(default_factory=list)


@dataclass
class ImportBlock(Node):
    """@import "path/to/file.mup" — reserved"""
    path: str = ""


# ============================================================
# Rich features (Phase 5)
# ============================================================

@dataclass
class ComponentDef(Node):
    """@def Name(param1, param2) ... @end"""
    name: str = ""
    params: List[str] = field(default_factory=list)
    children: List[Node] = field(default_factory=list)


@dataclass
class ComponentCall(Node):
    """@Name(param1="value", param2="value")"""
    name: str = ""
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChartBlock(Node):
    """@chart(type="bar") data: [...] labels: [...] @end"""
    chart_type: str = "bar"
    data: List = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    title: str = ""
    color: str = ""


@dataclass
class MathBlock(Node):
    """$$ E = mc^2 $$"""
    latex: str = ""
    display: bool = True


@dataclass
class TabsBlock(Node):
    """@tabs @tab "Title" ... @end @end"""
    tabs: List = field(default_factory=list)


@dataclass
class CollapseBlock(Node):
    """@collapse @item "Title" ... @end @end"""
    items: List = field(default_factory=list)


@dataclass
class AlertBlock(Node):
    """@note / @warning / @tip / @danger / @success ... @end"""
    alert_type: str = "note"
    children: List[Node] = field(default_factory=list)


@dataclass
class QuoteBlock(Node):
    """@quote(author="...", source="...") Text... @end"""
    author: str = ""
    source: str = ""
    text: str = ""


@dataclass
class TimelineBlock(Node):
    """@timeline date: text @end"""
    events: List = field(default_factory=list)


# ============================================================
# Inline-level nodes
# ============================================================

@dataclass
class Text(Node):
    content: str = ""


@dataclass
class Bold(Node):
    content: str = ""


@dataclass
class Italic(Node):
    content: str = ""


@dataclass
class InlineCode(Node):
    content: str = ""


@dataclass
class Strikethrough(Node):
    content: str = ""


@dataclass
class Link(Node):
    text: str = ""
    url: str = ""
    title: str = ""


@dataclass
class AutoLink(Node):
    url: str = ""
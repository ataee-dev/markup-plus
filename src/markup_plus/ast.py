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
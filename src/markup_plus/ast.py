"""
Markup+ Abstract Syntax Tree (AST)

Defines node types that represent the structure of a Markup+ document.

Phase 1 nodes:
    - Document (root)
    - Heading
    - Paragraph
    - Text (inline)
    - Bold (inline)
    - Italic (inline)
    - InlineCode (inline)
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


# ============================================================
# Inline-level nodes (used inside paragraphs and headings)
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
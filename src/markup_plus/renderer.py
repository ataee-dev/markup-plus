"""
Markup+ Renderer (Phase 1)

Converts an AST Document into HTML output.

Phase 1 handles:
    - Headings
    - Paragraphs
    - Inline formatting (bold, italic, inline code)
"""

import html
import re

from .ast import (
    Document,
    Heading,
    Paragraph,
    Node,
)

# ============================================================
# Inline formatting
# ============================================================

# Order matters: bold before italic so ** is not confused with *
RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
RE_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
RE_CODE = re.compile(r"`([^`]+?)`")


def render_inline(text: str) -> str:
    """
    Render inline formatting inside a text string.

    Applies, in order:
        - HTML escape
        - Inline code
        - Bold
        - Italic
    """
    # Escape HTML first (except for our own tags)
    text = html.escape(text, quote=False)

    # Inline code: `code`
    text = RE_CODE.sub(r"<code>\1</code>", text)

    # Bold: **text**
    text = RE_BOLD.sub(r"<strong>\1</strong>", text)

    # Italic: *text*
    text = RE_ITALIC.sub(r"<em>\1</em>", text)

    return text


# ============================================================
# Block rendering
# ============================================================

def render_node(node: Node) -> str:
    """Render a single AST node to HTML."""
    if isinstance(node, Heading):
        level = max(1, min(node.level, 6))
        return f"<h{level}>{render_inline(node.text)}</h{level}>"

    if isinstance(node, Paragraph):
        return f"<p>{render_inline(node.text)}</p>"

    # Unknown node — render nothing
    return ""


def render_ast(doc: Document) -> str:
    """Render a Document AST to HTML body (no wrapper)."""
    parts = [render_node(child) for child in doc.children]
    return "\n".join(p for p in parts if p)


# ============================================================
# Public API
# ============================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.7;
            color: #333;
            background: #fafafa;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #7c3aed;
            margin-top: 1.8em;
        }}
        h1 {{
            border-bottom: 2px solid #7c3aed;
            padding-bottom: 10px;
        }}
        code {{
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "Courier New", monospace;
            color: #d63384;
            font-size: 0.9em;
        }}
        strong {{ color: #1a1a1a; }}
        em {{ color: #555; }}
    </style>
</head>
<body>
{body}
</body>
</html>
"""


def to_html(text: str, title: str = "Markup+ Document") -> str:
    """
    Convert Markup+ source text to a complete HTML page.

    Args:
        text: Markup+ source text.
        title: HTML page title.

    Returns:
        Full HTML document as a string.
    """
    # Import here to avoid circular import at module load
    from .parser import parse_text

    doc = parse_text(text)
    body = render_ast(doc)
    return HTML_TEMPLATE.format(title=html.escape(title), body=body)
"""
Markup+ Renderer

Converts an AST Document into HTML output.
"""

import html
import re

from .ast import (
    BlockQuote,
    Document,
    Heading,
    HorizontalRule,
    ListBlock,
    Paragraph,
    Node,
)

# ============================================================
# Inline formatting
# ============================================================

RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
RE_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
RE_CODE = re.compile(r"`([^`]+?)`")


def render_inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = RE_CODE.sub(r"<code>\1</code>", text)
    text = RE_BOLD.sub(r"<strong>\1</strong>", text)
    text = RE_ITALIC.sub(r"<em>\1</em>", text)
    return text


# ============================================================
# Block rendering
# ============================================================

def render_node(node: Node) -> str:
    if isinstance(node, Heading):
        level = max(1, min(node.level, 6))
        return f"<h{level}>{render_inline(node.text)}</h{level}>"

    if isinstance(node, Paragraph):
        return f"<p>{render_inline(node.text)}</p>"

    if isinstance(node, ListBlock):
        tag = "ol" if node.ordered else "ul"
        items_html = "\n".join(
            f"  <li>{render_inline(item)}</li>" for item in node.items
        )
        return f"<{tag}>\n{items_html}\n</{tag}>"

    if isinstance(node, BlockQuote):
        # Multi-line quote: join with <br>, or use <p> per line
        lines = node.text.split("\n")
        inner = "\n".join(f"<p>{render_inline(line)}</p>" for line in lines)
        return f"<blockquote>\n{inner}\n</blockquote>"

    if isinstance(node, HorizontalRule):
        return "<hr>"

    return ""


def render_ast(doc: Document) -> str:
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
        ul, ol {{
            padding-left: 1.5em;
            margin: 1em 0;
        }}
        li {{ margin: 0.3em 0; }}
        blockquote {{
            border-left: 4px solid #7c3aed;
            background: #f8f5ff;
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #555;
            border-radius: 0 8px 8px 0;
        }}
        blockquote p {{
            margin: 0.3em 0;
        }}
        hr {{
            border: none;
            border-top: 2px dashed #ccc;
            margin: 2em 0;
        }}
    </style>
</head>
<body>
{body}
</body>
</html>
"""


def to_html(text: str, title: str = "Markup+ Document") -> str:
    from .parser import parse_text

    doc = parse_text(text)
    body = render_ast(doc)
    return HTML_TEMPLATE.format(title=html.escape(title), body=body)
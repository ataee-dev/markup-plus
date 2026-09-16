"""
Markup+ Renderer

Converts an AST Document into HTML output.

Features:
    - Light + Dark themes (CLI: --dark / --light)
    - RTL auto-detection (Persian, Arabic, Hebrew)
    - Headings, paragraphs, lists, blockquotes, HR
    - Enhanced code blocks with copy/download/preview
    - Images with lightbox, zoom, and description
    - Galleries with lightbox, keyboard nav, zoom toolbar
    - Inline links, autolinks, strikethrough
    - Tables with alignment
    - Task lists (checkboxes)
    - Front matter
    - Auto Table of Contents (@toc)
    - Footnotes [^1]
    - Phase 4: Variables (@let), If/Elif/Else, Each loops, Filters, Comments
    - Native-like smooth animations
    - Scroll reveal animations
"""

import html
import re
import unicodedata
import operator as _op
from typing import Any, List

from .ast import (
    BlockQuote,
    CodeBlock,
    Document,
    EachBlock,
    GalleryBlock,
    Heading,
    HorizontalRule,
    IfBlock,
    ImageBlock,
    ListBlock,
    Paragraph,
    TableBlock,
    TOCBlock,
    VariableDef,
    Node,
)


# ============================================================
# RTL Detection
# ============================================================

def is_rtl_text(text: str) -> bool:
    """Detect if text is predominantly RTL (Arabic, Hebrew, Persian, Urdu)."""
    if not text:
        return False

    rtl_count = 0
    ltr_count = 0

    for char in text:
        if not char.isalpha():
            continue
        try:
            bidi = unicodedata.bidirectional(char)
            if bidi in ("R", "AL", "AN"):
                rtl_count += 1
            elif bidi == "L":
                ltr_count += 1
        except (TypeError, ValueError):
            continue

    total = rtl_count + ltr_count
    if total == 0:
        return False
    return (rtl_count / total) >= 0.3


# ============================================================
# Inline formatting
# ============================================================

RE_CODE_INLINE = re.compile(r"`([^`]+?)`")
RE_STRIKE = re.compile(r"~~(.+?)~~")
RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
RE_ITALIC = re.compile(r"(?<!\*)\*([^*]+?)\*(?!\*)")
RE_LINK = re.compile(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)')
RE_AUTOLINK = re.compile(r"<(https?://[^\s>]+)>")
RE_FOOTNOTE_REF = re.compile(r"\[\^([^\]]+)\]")


def render_inline(text: str) -> str:
    """Render inline formatting inside a text string."""
    # Stash autolinks
    autolinks = []

    def stash_autolink(m):
        idx = len(autolinks)
        autolinks.append(m.group(1))
        return f"\x00AUTOLINK{idx}\x00"

    text = RE_AUTOLINK.sub(stash_autolink, text)

    # HTML escape
    text = html.escape(text, quote=False)

    # Inline code
    text = RE_CODE_INLINE.sub(r"<code>\1</code>", text)
    # Strikethrough
    text = RE_STRIKE.sub(r"<del>\1</del>", text)
    # Bold
    text = RE_BOLD.sub(r"<strong>\1</strong>", text)
    # Italic
    text = RE_ITALIC.sub(r"<em>\1</em>", text)

    # Footnote references
    def footnote_repl(m):
        key = m.group(1)
        return (
            f'<sup class="footnote-ref">'
            f'<a href="#fn-{html.escape(key)}" '
            f'id="fnref-{html.escape(key)}">'
            f'[{html.escape(key)}]'
            f"</a></sup>"
        )

    text = RE_FOOTNOTE_REF.sub(footnote_repl, text)

    # Links
    def link_repl(m):
        link_text = m.group(1)
        url = m.group(2)
        title = m.group(3)
        url_escaped = html.escape(url, quote=True)
        title_attr = f' title="{html.escape(title, quote=True)}"' if title else ""
        return (
            f'<a href="{url_escaped}"{title_attr} '
            f'target="_blank" rel="noopener noreferrer">{link_text}</a>'
        )

    text = RE_LINK.sub(link_repl, text)

    # Restore autolinks
    for idx, url in enumerate(autolinks):
        url_escaped = html.escape(url, quote=True)
        replacement = (
            f'<a href="{url_escaped}" '
            f'target="_blank" rel="noopener noreferrer">{url}</a>'
        )
        text = text.replace(f"\x00AUTOLINK{idx}\x00", replacement)

    return text


# ============================================================
# SVG Icons
# ============================================================

SVG_COPY = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>'
    '<path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>'
    "</svg>"
)

SVG_DOWNLOAD = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
    '<polyline points="7 10 12 15 17 10"/>'
    '<line x1="12" y1="15" x2="12" y2="3"/>'
    "</svg>"
)

SVG_EYE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>'
    '<circle cx="12" cy="12" r="3"/>'
    "</svg>"
)

SVG_CODE = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" '
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<polyline points="16 18 22 12 16 6"/>'
    '<polyline points="8 6 2 12 8 18"/>'
    "</svg>"
)


# ============================================================
# Code block rendering
# ============================================================

def render_code_block(node: CodeBlock) -> str:
    """Render a CodeBlock with header (language + buttons) and code."""
    lang = node.language or "text"
    code_escaped = html.escape(node.code, quote=False)

    previewable = lang.lower() in ("html", "css", "javascript", "js")
    rtl_langs = ("ar", "he", "fa", "ur", "yi")
    is_rtl = lang.lower() in rtl_langs

    if node.title:
        left = (
            f'<span class="code-icon">{SVG_CODE}</span>'
            f'<span class="code-title">{html.escape(node.title)}</span>'
        )
    else:
        left = (
            f'<span class="code-icon">{SVG_CODE}</span>'
            f'<span class="code-lang">{lang}</span>'
        )

    buttons = []

    if previewable:
        buttons.append(
            '<button class="code-btn" data-action="preview" '
            'title="Preview" aria-label="Preview">'
            f'{SVG_EYE}<span class="code-btn-label">Preview</span>'
            "</button>"
        )

    if node.copy:
        buttons.append(
            '<button class="code-btn" data-action="copy" '
            'title="Copy to clipboard" aria-label="Copy">'
            f'{SVG_COPY}<span class="code-btn-label">Copy</span>'
            "</button>"
        )

    if node.download:
        filename = node.title or f"code.{lang}"
        buttons.append(
            f'<button class="code-btn" data-action="download" '
            f'data-filename="{html.escape(filename)}" '
            f'title="Download" aria-label="Download">'
            f'{SVG_DOWNLOAD}<span class="code-btn-label">Download</span>'
            f"</button>"
        )

    buttons_html = "".join(buttons)

    wrap_class = " wrap" if node.wrap else ""
    previewable_class = " previewable" if previewable else ""
    rtl_class = " rtl" if is_rtl else ""

    preview_data_attr = ""
    if previewable:
        preview_data_attr = (
            f' data-preview-lang="{lang}"'
            f' data-preview-code="{html.escape(node.code, quote=True)}"'
        )

    return (
        f'<div class="code-block reveal{wrap_class}{previewable_class}{rtl_class}" '
        f'data-lang="{lang}"{preview_data_attr}>'
        f'<div class="code-header">'
        f'<div class="code-header-left">{left}</div>'
        f'<div class="code-buttons">{buttons_html}</div>'
        f"</div>"
        f'<div class="code-body">'
        f'<pre><code class="language-{lang}">{code_escaped}</code></pre>'
        f"</div>"
        f'<div class="code-preview" hidden></div>'
        f"</div>"
    )


# ============================================================
# Image rendering
# ============================================================

def render_image(node: ImageBlock) -> str:
    """Render a single image with optional lightbox support."""
    attrs = [
        f'src="{html.escape(node.url, quote=True)}"',
        f'alt="{html.escape(node.alt, quote=True)}"',
    ]

    if node.title:
        attrs.append(f'title="{html.escape(node.title, quote=True)}"')
    if node.width:
        attrs.append(f'width="{html.escape(node.width, quote=True)}"')
    if node.height:
        attrs.append(f'height="{html.escape(node.height, quote=True)}"')

    img_tag = f'<img {" ".join(attrs)} loading="lazy">'

    caption = node.caption or node.alt
    description = node.description

    if node.zoomable and not node.link:
        inner = (
            f'<div class="image-single reveal" '
            f'data-src="{html.escape(node.url, quote=True)}" '
            f'data-caption="{html.escape(caption, quote=True)}" '
            f'data-description="{html.escape(description, quote=True)}">'
            f"{img_tag}"
            f'<div class="image-single-overlay"></div>'
            f"</div>"
        )
    else:
        if node.link:
            img_tag = (
                f'<a href="{html.escape(node.link, quote=True)}" '
                f'target="_blank" rel="noopener noreferrer">{img_tag}</a>'
            )
        inner = f'<div class="image-single-static reveal">{img_tag}</div>'

    if node.caption or node.description:
        caption_parts = []
        if node.caption:
            caption_parts.append(
                f'<figcaption class="image-caption">'
                f"{render_inline(node.caption)}"
                f"</figcaption>"
            )
        if node.description:
            caption_parts.append(
                f'<div class="image-description">'
                f"{render_inline(node.description)}"
                f"</div>"
            )

        inner = (
            f'<figure class="image-figure reveal">'
            f"{inner}"
            f'{"".join(caption_parts)}'
            f"</figure>"
        )

    align = (node.align or "").lower()
    if align in ("center", "left", "right"):
        return f'<div class="image-align-{align} reveal">{inner}</div>'

    return inner


# ============================================================
# Gallery rendering
# ============================================================

def render_gallery(node: GalleryBlock) -> str:
    """Render a gallery of images with lightbox support."""
    if not node.images:
        return ""

    gallery_id = f"gallery-{id(node) % 1000000}"
    items = []

    for i, img in enumerate(node.images):
        img_attrs = [
            f'src="{html.escape(img.url, quote=True)}"',
            f'alt="{html.escape(img.alt, quote=True)}"',
        ]
        if img.title:
            img_attrs.append(f'title="{html.escape(img.title, quote=True)}"')

        img_tag = f'<img {" ".join(img_attrs)} loading="lazy">'
        caption = img.caption or img.alt
        description = img.description

        items.append(
            f'<div class="gallery-item reveal" '
            f'data-index="{i}" '
            f'data-src="{html.escape(img.url, quote=True)}" '
            f'data-caption="{html.escape(caption, quote=True)}" '
            f'data-description="{html.escape(description, quote=True)}">'
            f"{img_tag}"
            f'<div class="gallery-item-overlay"></div>'
            f"</div>"
        )

    grid = "\n".join(items)

    caption_html = ""
    if node.caption:
        caption_html = (
            f'<figcaption class="gallery-caption">'
            f'{render_inline(node.caption)}'
            f"</figcaption>"
        )

    columns = max(1, min(node.columns, 6))

    return (
        f'<figure class="gallery reveal" id="{gallery_id}">'
        f'<div class="gallery-grid" '
        f'style="grid-template-columns: repeat({columns}, minmax(0, 1fr));">'
        f"{grid}"
        f"</div>"
        f"{caption_html}"
        f"</figure>"
    )


# ============================================================
# Table rendering
# ============================================================

def render_table(node: TableBlock, context: dict = None) -> str:
    """Render a table with alignment + variable substitution."""
    if context is None:
        context = {}

    if not node.headers:
        return ""

    header_cells = []
    for i, h in enumerate(node.headers):
        align = node.alignments[i] if i < len(node.alignments) else "none"
        style = ""
        if align == "center":
            style = ' style="text-align: center;"'
        elif align == "right":
            style = ' style="text-align: right;"'
        elif align == "left":
            style = ' style="text-align: left;"'
        text = substitute_variables(h, context)
        header_cells.append(f"<th{style}>{render_inline(text)}</th>")

    header_html = (
        "  <thead>\n    <tr>\n      "
        + "\n      ".join(header_cells)
        + "\n    </tr>\n  </thead>"
    )

    body_rows = []
    for row in node.rows:
        cells = []
        for i, cell in enumerate(row):
            align = node.alignments[i] if i < len(node.alignments) else "none"
            style = ""
            if align == "center":
                style = ' style="text-align: center;"'
            elif align == "right":
                style = ' style="text-align: right;"'
            elif align == "left":
                style = ' style="text-align: left;"'
            text = substitute_variables(cell, context)
            cells.append(f"<td{style}>{render_inline(text)}</td>")
        body_rows.append(
            "    <tr>\n      " + "\n      ".join(cells) + "\n    </tr>"
        )

    body_html = "  <tbody>\n" + "\n".join(body_rows) + "\n  </tbody>"

    return (
        f'<div class="table-wrapper reveal">'
        f"<table>\n{header_html}\n{body_html}\n</table>"
        f"</div>"
    )


# ============================================================
# TOC rendering
# ============================================================

def render_toc(node: TOCBlock, doc: Document) -> str:
    """Render a table of contents from all headings in the document."""
    headings = []

    def collect(children):
        for child in children:
            if isinstance(child, Heading):
                headings.append(child)
            elif isinstance(child, IfBlock):
                for _, branch_children in child.branches:
                    collect(branch_children)
            elif isinstance(child, EachBlock):
                collect(child.children)

    collect(doc.children)

    if not headings:
        return ""

    title = getattr(node, "title", "") or "Table of Contents"
    min_level = min(h.level for h in headings)
    items = []

    for h in headings:
        indent = h.level - min_level
        slug = h.slug or ""
        items.append(
            f'<li class="toc-item toc-level-{h.level}" '
            f'style="padding-left: {indent * 1.2}em;">'
            f'<a href="#{html.escape(slug)}">{render_inline(h.text)}</a>'
            f"</li>"
        )

    return (
        f'<nav class="toc reveal" aria-label="Table of Contents">'
        f'<div class="toc-title">{html.escape(title)}</div>'
        f'<ul class="toc-list">'
        f'{"".join(items)}'
        f"</ul>"
        f"</nav>"
    )


# ============================================================
# Footnotes rendering
# ============================================================

def render_footnotes(doc: Document) -> str:
    """Render the footnotes section at the bottom if any exist."""
    if not doc.footnotes:
        return ""

    items = []
    for key in sorted(doc.footnotes.keys()):
        text = doc.footnotes[key]
        items.append(
            f'<li class="footnote-item" id="fn-{html.escape(key)}">'
            f'<span class="footnote-number">[{html.escape(key)}]</span> '
            f'<span class="footnote-text">{render_inline(text)}</span> '
            f'<a href="#fnref-{html.escape(key)}" class="footnote-back" '
            f'aria-label="Back to reference">↩</a>'
            f"</li>"
        )

    return (
        f'<section class="footnotes reveal" aria-label="Footnotes">'
        f'<hr class="footnotes-sep">'
        f'<ol class="footnotes-list">'
        f'{"".join(items)}'
        f"</ol>"
        f"</section>"
    )


# ============================================================
# Expression evaluator (Phase 4)
# ============================================================

_OPERATORS = [
    ("==", _op.eq),
    ("!=", _op.ne),
    (">=", _op.ge),
    ("<=", _op.le),
    (">", _op.gt),
    ("<", _op.lt),
]


def _parse_literal(token: str, variables: dict) -> Any:
    """Parse a single literal or variable name."""
    token = token.strip()
    if token == "":
        return ""

    if (token.startswith('"') and token.endswith('"')) or \
       (token.startswith("'") and token.endswith("'")):
        return token[1:-1]

    if token.lower() == "true":
        return True
    if token.lower() == "false":
        return False
    if token.lower() in ("none", "null"):
        return None

    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        pass

    if token in variables:
        return variables[token]

    return token


def _tokenize_expr(expr: str) -> list:
    """Tokenize an expression into parts."""
    tokens = []
    current = []
    in_quote = None
    i = 0

    while i < len(expr):
        ch = expr[i]

        if in_quote:
            current.append(ch)
            if ch == in_quote:
                in_quote = None
            i += 1
            continue

        if ch in ('"', "'"):
            in_quote = ch
            current.append(ch)
            i += 1
            continue

        if i + 1 < len(expr):
            two = expr[i:i+2]
            if two in ("==", "!=", ">=", "<="):
                if current:
                    tokens.append("".join(current).strip())
                    current = []
                tokens.append(two)
                i += 2
                continue

        if ch in "><":
            if current:
                tokens.append("".join(current).strip())
                current = []
            tokens.append(ch)
            i += 1
            continue

        if ch.isspace():
            if current:
                tokens.append("".join(current).strip())
                current = []
            i += 1
            continue

        current.append(ch)
        i += 1

    if current:
        tokens.append("".join(current).strip())

    return [t for t in tokens if t != ""]


def evaluate_condition(expr: str, variables: dict) -> bool:
    """Evaluate a condition expression like `x == 5` or `name != "Ali"`."""
    expr = expr.strip()
    if not expr:
        return False

    parts = _tokenize_expr(expr)

    if len(parts) == 1:
        value = _parse_literal(parts[0], variables)
        return bool(value)

    if len(parts) == 3:
        left_tok, op_str, right_tok = parts
        left = _parse_literal(left_tok, variables)
        right = _parse_literal(right_tok, variables)

        for op_name, op_fn in _OPERATORS:
            if op_str == op_name:
                try:
                    return bool(op_fn(left, right))
                except (TypeError, ValueError):
                    return False
        return False

    return bool(_parse_literal(expr, variables))


def evaluate_iterable(expr: str, variables: dict) -> list:
    """Evaluate the iterable expression in @each."""
    expr = expr.strip()

    if expr in variables:
        value = variables[expr]
        if isinstance(value, (list, tuple)):
            return list(value)
        return [value]

    if expr.startswith("[") and expr.endswith("]"):
        inner = expr[1:-1].strip()
        if not inner:
            return []
        items = []
        current = []
        in_quote = None
        depth = 0

        for ch in inner:
            if in_quote:
                current.append(ch)
                if ch == in_quote:
                    in_quote = None
                continue
            if ch in ('"', "'"):
                in_quote = ch
                current.append(ch)
                continue
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
            elif ch == "," and depth == 0:
                items.append("".join(current).strip())
                current = []
                continue
            current.append(ch)

        if current:
            items.append("".join(current).strip())

        return [_parse_literal(item, variables) for item in items]

    return []


def apply_filters(value: Any, filters: List[str]) -> Any:
    """Apply filters like `upper`, `lower`, `length`, `reverse`."""
    for f in filters:
        f = f.strip().lower()
        if f == "upper":
            value = str(value).upper()
        elif f == "lower":
            value = str(value).lower()
        elif f == "length":
            try:
                value = len(value)
            except TypeError:
                value = 0
        elif f == "reverse":
            if isinstance(value, (list, tuple)):
                value = list(reversed(value))
            else:
                value = str(value)[::-1]
        elif f == "capitalize":
            value = str(value).capitalize()
        elif f == "title":
            value = str(value).title()
    return value


RE_VAR_WITH_FILTERS = re.compile(
    r"\{([A-Za-z_][\w]*)((?:\s*\|\s*\w+)*)\}"
)


def substitute_variables(text: str, variables: dict) -> str:
    """Replace {var} and {var | filter | filter} placeholders."""
    if not text or not isinstance(text, str):
        return text

    def repl(m):
        name = m.group(1)
        filters_str = m.group(2) or ""
        filters = [f.strip() for f in filters_str.split("|") if f.strip()]

        if name in variables:
            value = variables[name]
        else:
            if not filters:
                return m.group(0)
            value = ""

        if filters:
            value = apply_filters(value, filters)

        if value is None:
            return ""
        return str(value)

    return RE_VAR_WITH_FILTERS.sub(repl, text)


# ============================================================
# Block rendering (with context)
# ============================================================

def render_node(node: Node, doc: Document = None, context: dict = None) -> str:
    """Render a single node with optional context (for @each/@if)."""
    if context is None:
        context = {}

    if isinstance(node, Heading):
        level = max(1, min(node.level, 6))
        slug = getattr(node, "slug", "") or ""
        id_attr = f' id="{html.escape(slug)}"' if slug else ""
        text = substitute_variables(node.text, context)
        return (
            f'<h{level}{id_attr} class="reveal">'
            f'{render_inline(text)}'
            f'</h{level}>'
        )

    if isinstance(node, Paragraph):
        text = substitute_variables(node.text, context)
        return f'<p class="reveal">{render_inline(text)}</p>'

    if isinstance(node, ListBlock):
        tag = "ol" if node.ordered else "ul"
        has_tasks = any(c is not None for c in node.checked) if node.checked else False
        extra_class = ' class="task-list reveal"' if has_tasks else ' class="reveal"'

        items_html_parts = []
        for i, item in enumerate(node.items):
            checked = node.checked[i] if i < len(node.checked) else None
            text = substitute_variables(item, context)
            if checked is True:
                items_html_parts.append(
                    f'  <li class="task-done">{render_inline(text)}</li>'
                )
            elif checked is False:
                items_html_parts.append(
                    f'  <li class="task-todo">{render_inline(text)}</li>'
                )
            else:
                items_html_parts.append(f"  <li>{render_inline(text)}</li>")

        items_html = "\n".join(items_html_parts)
        return f'<{tag}{extra_class}>\n{items_html}\n</{tag}>'

    if isinstance(node, BlockQuote):
        text = substitute_variables(node.text, context)
        lines = text.split("\n")
        inner = "\n".join(f"<p>{render_inline(line)}</p>" for line in lines)
        return f'<blockquote class="reveal">\n{inner}\n</blockquote>'

    if isinstance(node, HorizontalRule):
        return '<hr class="reveal">'

    if isinstance(node, CodeBlock):
        return render_code_block(node)

    if isinstance(node, ImageBlock):
        return render_image(node)

    if isinstance(node, GalleryBlock):
        return render_gallery(node)

    if isinstance(node, TableBlock):
        return render_table(node, context)

    if isinstance(node, TOCBlock) and doc is not None:
        return render_toc(node, doc)

    if isinstance(node, VariableDef):
        return ""

    if isinstance(node, IfBlock):
        return render_if_block(node, doc, context)

    if isinstance(node, EachBlock):
        return render_each_block(node, doc, context)

    return ""


def render_if_block(node: IfBlock, doc: Document, context: dict) -> str:
    """Render @if block by evaluating conditions."""
    for condition, children in node.branches:
        if condition is None:
            return _render_children(children, doc, context)
        if evaluate_condition(condition, context):
            return _render_children(children, doc, context)
    return ""


def render_each_block(node: EachBlock, doc: Document, context: dict) -> str:
    """Render @each block by iterating over the iterable."""
    items = evaluate_iterable(node.iterable_expr, context)

    parts = []
    for i, item in enumerate(items):
        child_ctx = dict(context)
        child_ctx[node.item_name] = item
        if node.index_name:
            child_ctx[node.index_name] = i
        parts.append(_render_children(node.children, doc, child_ctx))

    return "\n".join(parts)


def _render_children(children: list, doc: Document, context: dict) -> str:
    """Render a list of children with a given context."""
    parts = []
    for child in children:
        rendered = render_node(child, doc, context)
        if rendered:
            parts.append(rendered)
    return "\n".join(parts)


def render_ast(doc: Document) -> str:
    """Render the document AST to HTML body."""
    # Build root context: meta + variables
    context = dict(doc.meta) if doc.meta else {}
    context.update(doc.variables)

    parts = []
    for child in doc.children:
        rendered = render_node(child, doc, context)
        if rendered:
            parts.append(rendered)

    body = "\n".join(parts)

    # Append footnotes
    footnotes_html = render_footnotes(doc)
    if footnotes_html:
        body += "\n" + footnotes_html

    return body


# ============================================================
# HTML Template
# ============================================================

HEAD = """<!DOCTYPE html>
<html lang="__LANG__" dir="__DIR__" data-theme="__THEME__">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>

    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css"
          id="prism-theme">
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-markup.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-css.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-typescript.min.js"></script>

    <style>
        :root,
        [data-theme="light"] {
            --bg-page: #ffffff;
            --bg-soft: #f4f4f5;
            --bg-code: #f6f8fa;
            --bg-code-header: #eaedf0;
            --bg-blockquote: #f8f5ff;
            --bg-preview: #fafafa;
            --bg-table-alt: #f9f9fb;
            --bg-table-header: #f4f4f5;

            --text-main: #18181b;
            --text-soft: #52525b;
            --text-muted: #71717a;

            --border: #e4e4e7;
            --border-code: #d0d7de;
            --border-table: #e4e4e7;

            --accent: #7c3aed;
            --accent-soft: rgba(124, 58, 237, 0.08);
            --accent-hover: #5b21b6;
            --accent-rgb: 124, 58, 237;

            --code-text: #24292f;
            --code-accent: #0969da;
            --code-border: #d0d7de;

            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.12);
            --shadow-xl: 0 24px 60px rgba(0, 0, 0, 0.18);
        }

        [data-theme="dark"] {
            --bg-page: #0a0a0f;
            --bg-soft: #131318;
            --bg-code: #18181b;
            --bg-code-header: #131318;
            --bg-blockquote: rgba(167, 139, 250, 0.08);
            --bg-preview: #1a1a20;
            --bg-table-alt: #131318;
            --bg-table-header: #18181b;

            --text-main: #e4e4e7;
            --text-soft: #d4d4d8;
            --text-muted: #a1a1aa;

            --border: rgba(255, 255, 255, 0.1);
            --border-code: rgba(255, 255, 255, 0.06);
            --border-table: rgba(255, 255, 255, 0.1);

            --accent: #a78bfa;
            --accent-soft: rgba(167, 139, 250, 0.12);
            --accent-hover: #ec4899;
            --accent-rgb: 167, 139, 250;

            --code-text: #e4e4e7;
            --code-accent: #a78bfa;
            --code-border: rgba(255, 255, 255, 0.08);

            --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.5);
            --shadow-xl: 0 30px 80px rgba(0, 0, 0, 0.6);
        }

        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        html, body { margin: 0; padding: 0; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", "Vazirmatn", Tahoma, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 24px 80px;
            line-height: 1.75;
            color: var(--text-main);
            background: var(--bg-page);
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            transition:
                background 0.5s cubic-bezier(0.4, 0, 0.2, 1),
                color 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--accent);
            margin-top: 1.8em;
            font-weight: 700;
            letter-spacing: -0.02em;
            transition: color 0.3s ease;
        }

        h1 {
            font-size: 2.2em;
            border-bottom: 2px solid var(--accent-soft);
            padding-bottom: 12px;
        }

        [data-theme="dark"] h1 {
            background: linear-gradient(135deg, #a78bfa, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            border-bottom-color: rgba(167, 139, 250, 0.3);
        }

        code {
            background: var(--accent-soft);
            padding: 2px 7px;
            border-radius: 5px;
            font-family: "JetBrains Mono", "Courier New", monospace;
            color: var(--accent);
            font-size: 0.88em;
            transition: background 0.3s ease, color 0.3s ease;
        }

        strong { color: var(--text-main); font-weight: 700; }
        em { color: var(--text-soft); font-style: italic; }

        del {
            color: var(--text-muted);
            text-decoration: line-through;
            opacity: 0.75;
        }

        ul, ol { padding-left: 1.5em; margin: 1em 0; color: var(--text-soft); }
        li { margin: 0.4em 0; }

        blockquote {
            border-left: 4px solid var(--accent);
            background: var(--bg-blockquote);
            margin: 1.5em 0;
            padding: 0.8em 1.2em;
            color: var(--text-soft);
            border-radius: 0 10px 10px 0;
            transition: background 0.3s ease;
        }

        blockquote p { margin: 0.4em 0; }

        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 2.5em 0;
            transition: border-color 0.3s ease;
        }

        a {
            color: var(--accent);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: color 0.2s ease, border-bottom-color 0.2s ease;
        }

        a:hover {
            color: var(--accent-hover);
            border-bottom-color: currentColor;
        }

        .reveal {
            opacity: 0;
            transform: translateY(30px);
            transition:
                opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
            will-change: opacity, transform;
        }

        .reveal.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .gallery-grid .reveal:nth-child(1) { transition-delay: 0.00s; }
        .gallery-grid .reveal:nth-child(2) { transition-delay: 0.06s; }
        .gallery-grid .reveal:nth-child(3) { transition-delay: 0.12s; }
        .gallery-grid .reveal:nth-child(4) { transition-delay: 0.18s; }
        .gallery-grid .reveal:nth-child(5) { transition-delay: 0.24s; }
        .gallery-grid .reveal:nth-child(6) { transition-delay: 0.30s; }
        .gallery-grid .reveal:nth-child(7) { transition-delay: 0.36s; }
        .gallery-grid .reveal:nth-child(8) { transition-delay: 0.42s; }
        .gallery-grid .reveal:nth-child(n+9) { transition-delay: 0.48s; }

        ul.task-list,
        ol.task-list {
            list-style: none;
            padding-left: 0;
        }

        ul.task-list li,
        ol.task-list li {
            display: flex;
            align-items: flex-start;
            gap: 0.6em;
            padding-left: 0;
        }

        ul.task-list li::before,
        ol.task-list li::before {
            content: "";
            flex-shrink: 0;
            width: 18px;
            height: 18px;
            margin-top: 0.35em;
            border: 2px solid var(--border);
            border-radius: 5px;
            background: var(--bg-page);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        ul.task-list li.task-done::before,
        ol.task-list li.task-done::before {
            content: "✓";
            background: var(--accent);
            border-color: var(--accent);
            color: white;
            font-size: 12px;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
            padding-bottom: 1px;
        }

        ul.task-list li.task-done,
        ol.task-list li.task-done {
            color: var(--text-muted);
            text-decoration: line-through;
            opacity: 0.7;
        }

        .table-wrapper {
            margin: 1.8em 0;
            overflow-x: auto;
            border-radius: 12px;
            border: 1px solid var(--border-table);
            box-shadow: var(--shadow-sm);
            background: var(--bg-page);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.94em;
        }

        thead { background: var(--bg-table-header); }

        th {
            padding: 0.8em 1em;
            text-align: left;
            font-weight: 700;
            color: var(--text-main);
            border-bottom: 1px solid var(--border-table);
            white-space: nowrap;
        }

        td {
            padding: 0.7em 1em;
            color: var(--text-soft);
            border-bottom: 1px solid var(--border-table);
        }

        tbody tr:last-child td { border-bottom: none; }
        tbody tr:nth-child(even) { background: var(--bg-table-alt); }
        tbody tr { transition: background 0.2s ease; }
        tbody tr:hover { background: var(--accent-soft); }

        .image-single {
            position: relative;
            display: inline-block;
            max-width: 100%;
            border-radius: 12px;
            overflow: hidden;
            cursor: zoom-in;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .image-single img {
            display: block;
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1),
                        filter 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .image-single:hover {
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }

        .image-single:hover img {
            transform: scale(1.04);
            filter: grayscale(25%) brightness(0.88);
        }

        .image-single-overlay {
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.35);
            opacity: 0;
            transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 12px;
            pointer-events: none;
        }

        .image-single:hover .image-single-overlay { opacity: 1; }

        .image-single-static { display: inline-block; max-width: 100%; }
        .image-single-static img {
            display: block;
            max-width: 100%;
            height: auto;
            border-radius: 12px;
        }

        .image-align-center { display: flex; justify-content: center; margin: 1.5em 0; }
        .image-align-left { display: flex; justify-content: flex-start; margin: 1.5em 0; }
        .image-align-right { display: flex; justify-content: flex-end; margin: 1.5em 0; }

        .image-figure {
            margin: 1.5em 0;
            display: inline-block;
            text-align: center;
            max-width: 100%;
        }

        .image-figure .image-single,
        .image-figure .image-single-static { display: inline-block; }

        .image-caption {
            margin-top: 0.8em;
            font-size: 0.9em;
            color: var(--text-muted);
            font-style: italic;
            line-height: 1.5;
        }

        .image-description {
            margin-top: 0.4em;
            font-size: 0.85em;
            color: var(--text-muted);
            line-height: 1.5;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0.9;
        }

        p img {
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            vertical-align: middle;
        }

        .code-block {
            margin: 1.5em 0;
            border-radius: 12px;
            overflow: hidden;
            background: var(--bg-code);
            border: 1px solid var(--border-code);
            box-shadow: var(--shadow-sm), var(--shadow-md);
            transition:
                box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .code-block:hover {
            border-color: rgba(var(--accent-rgb), 0.4);
            box-shadow: var(--shadow-md), 0 16px 40px rgba(var(--accent-rgb), 0.12);
            transform: translateY(-2px);
        }

        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.65em 1em;
            background: var(--bg-code-header);
            border-bottom: 1px solid var(--border-code);
            color: var(--text-soft);
            font-size: 0.82em;
            transition: background 0.3s ease;
        }

        .code-header-left {
            display: flex;
            align-items: center;
            gap: 0.5em;
            min-width: 0;
        }

        .code-icon {
            display: inline-flex;
            align-items: center;
            color: var(--code-accent);
        }

        .code-lang {
            font-weight: 600;
            color: var(--code-accent);
            letter-spacing: 0.02em;
            text-transform: lowercase;
        }

        .code-title {
            font-family: "JetBrains Mono", "Courier New", monospace;
            font-weight: 600;
            color: var(--code-text);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .code-buttons { display: flex; gap: 0.3em; flex-shrink: 0; }

        .code-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.35em;
            background: transparent;
            border: 1px solid var(--code-border);
            border-radius: 6px;
            padding: 0.35em 0.7em;
            cursor: pointer;
            font-size: 0.85em;
            font-family: inherit;
            font-weight: 500;
            color: var(--code-text);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap;
        }

        .code-btn:hover {
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent);
            transform: translateY(-1px);
        }

        .code-btn:active { transform: translateY(0) scale(0.96); }
        .code-btn.success { border-color: #10b981; color: #10b981; }
        .code-btn.active {
            background: var(--accent-soft);
            border-color: var(--accent);
            color: var(--accent);
        }

        .code-btn svg {
            flex-shrink: 0;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .code-btn:hover svg { transform: scale(1.12); }
        .code-btn.success svg { animation: pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1); }
        .code-btn-label { font-size: 0.82em; }

        @keyframes pop {
            0% { transform: scale(1); }
            50% { transform: scale(1.4); }
            100% { transform: scale(1); }
        }

        .code-body { position: relative; overflow: hidden; }

        .code-block pre {
            margin: 0;
            border-radius: 0;
            background: var(--bg-code);
            padding: 1.2em 1.4em;
            overflow-x: auto;
            transition: background 0.3s ease;
        }

        .code-block pre code {
            background: transparent;
            color: var(--code-text);
            padding: 0;
            font-family: "JetBrains Mono", "Fira Code", "Courier New", monospace;
            font-size: 0.86em;
            line-height: 1.7;
        }

        .code-block.rtl pre { direction: rtl; }
        .code-block.rtl pre code {
            direction: rtl;
            text-align: right;
            font-family: "Vazirmatn", "Tahoma", "Segoe UI", sans-serif;
        }

        .code-block.wrap pre code {
            white-space: pre-wrap;
            word-break: break-word;
        }

        .code-preview {
            padding: 1.5em;
            background: var(--bg-preview);
            border-top: 1px solid var(--border-code);
            color: #222;
            animation: slideDown 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
        }

        .code-preview iframe {
            width: 100%;
            min-height: 240px;
            border: 1px solid var(--border);
            border-radius: 10px;
            background: #ffffff;
            display: block;
        }

        .code-preview * { max-width: 100%; }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-12px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .gallery { margin: 2.5em 0; }

        .gallery-grid {
            display: grid;
            gap: 14px;
            margin: 0;
        }

        .gallery-item {
            position: relative;
            overflow: hidden;
            border-radius: 12px;
            cursor: zoom-in;
            background: var(--bg-soft);
            aspect-ratio: 4 / 3;
            transition:
                transform 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                box-shadow 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .gallery-item:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
        }

        .gallery-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition:
                transform 0.7s cubic-bezier(0.4, 0, 0.2, 1),
                filter 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .gallery-item:hover img {
            transform: scale(1.12);
            filter: grayscale(50%) brightness(0.82);
        }

        .gallery-item-overlay {
            position: absolute;
            inset: 0;
            background: rgba(0, 0, 0, 0.4);
            opacity: 0;
            transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: none;
        }

        .gallery-item:hover .gallery-item-overlay { opacity: 1; }

        .gallery-caption {
            text-align: center;
            margin-top: 1em;
            font-size: 0.9em;
            color: var(--text-muted);
            font-style: italic;
        }

        .lightbox {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.95);
            z-index: 10000;
            display: none;
            align-items: center;
            justify-content: center;
            opacity: 0;
            transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            overflow: hidden;
        }

        .lightbox.active { display: flex; opacity: 1; }

        .lightbox-stage {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: auto;
            padding: 100px 100px 120px;
        }

        .lightbox-image-wrapper {
            position: relative;
            max-width: 100%;
            max-height: 100%;
            transform: scale(0.92);
            transition: transform 0.5s cubic-bezier(0.34, 1.2, 0.64, 1);
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .lightbox.active .lightbox-image-wrapper { transform: scale(1); }
        .lightbox-image-wrapper.zoomed { max-width: none; max-height: none; transform: scale(1); }

        #mup-lightbox-img {
            max-width: 100%;
            max-height: calc(100vh - 260px);
            object-fit: contain;
            display: block;
            border-radius: 12px;
            box-shadow: var(--shadow-xl);
            transition:
                opacity 0.25s ease,
                max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                max-width 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: zoom-in;
        }

        .lightbox-image-wrapper.zoomed #mup-lightbox-img {
            max-height: none;
            max-width: none;
            cursor: zoom-out;
        }

        .lightbox-info {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 30px 120px 100px;
            background: linear-gradient(to top, rgba(0, 0, 0, 0.95) 20%, transparent);
            text-align: center;
            pointer-events: none;
            opacity: 0;
            transform: translateY(24px);
            transition: opacity 0.45s cubic-bezier(0.4, 0, 0.2, 1), transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 10001;
        }

        .lightbox.active .lightbox-info { opacity: 1; transform: translateY(0); transition-delay: 0.15s; }

        .lightbox-caption {
            color: #ffffff;
            font-size: 1.05em;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .lightbox-caption:empty { display: none; }

        .lightbox-description {
            color: #a1a1aa;
            font-size: 0.9em;
            line-height: 1.6;
            max-width: 640px;
            margin: 0 auto;
        }

        .lightbox-description:empty { display: none; }

        .lightbox-close,
        .lightbox-prev,
        .lightbox-next {
            position: absolute;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: white;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.34, 1.2, 0.64, 1);
            z-index: 10002;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
        }

        .lightbox-close:hover,
        .lightbox-prev:hover,
        .lightbox-next:hover {
            background: rgba(255, 255, 255, 0.22);
            border-color: rgba(255, 255, 255, 0.4);
        }

        .lightbox-close { top: 24px; right: 24px; }
        .lightbox-close:hover { transform: scale(1.12) rotate(90deg); }
        .lightbox-prev { left: 24px; top: 50%; transform: translateY(-50%); }
        .lightbox-prev:hover { transform: translateY(-50%) scale(1.12) translateX(-4px); }
        .lightbox-next { right: 24px; top: 50%; transform: translateY(-50%); }
        .lightbox-next:hover { transform: translateY(-50%) scale(1.12) translateX(4px); }

        .lightbox-counter {
            position: absolute;
            top: 28px;
            left: 50%;
            transform: translateX(-50%) translateY(-20px);
            color: #ffffff;
            font-size: 0.85em;
            font-weight: 600;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 18px;
            border-radius: 24px;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            z-index: 10002;
            opacity: 0;
            transition: opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .lightbox.active .lightbox-counter { opacity: 1; transform: translateX(-50%) translateY(0); transition-delay: 0.1s; }

        .lightbox-toolbar {
            position: absolute;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%) translateY(24px);
            display: flex;
            gap: 6px;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 40px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            z-index: 10003;
            opacity: 0;
            transition: opacity 0.45s cubic-bezier(0.4, 0, 0.2, 1), transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .lightbox.active .lightbox-toolbar { opacity: 1; transform: translateX(-50%) translateY(0); transition-delay: 0.2s; }

        .lightbox-tool {
            background: transparent;
            border: none;
            color: #ffffff;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.25s cubic-bezier(0.34, 1.2, 0.64, 1);
        }

        .lightbox-tool:hover { background: rgba(255, 255, 255, 0.2); transform: scale(1.1); }
        .lightbox-tool:active { transform: scale(0.92); }

        /* ============================================================
           Table of Contents
           ============================================================ */

        .toc {
            margin: 2em 0;
            padding: 1.2em 1.5em;
            background: var(--bg-soft);
            border-radius: 12px;
            border: 1px solid var(--border);
        }

        .toc-title {
            font-weight: 700;
            color: var(--accent);
            font-size: 1.05em;
            margin-bottom: 0.8em;
            padding-bottom: 0.6em;
            border-bottom: 1px solid var(--border);
        }

        .toc-list { list-style: none; padding: 0; margin: 0; }

        .toc-item { margin: 0.35em 0; padding-left: 0; line-height: 1.5; }

        .toc-item a {
            color: var(--text-soft);
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: color 0.2s ease, border-bottom-color 0.2s ease;
        }

        .toc-item a:hover { color: var(--accent); border-bottom-color: currentColor; }

        .toc-level-1 { font-weight: 600; margin-top: 0.6em; }
        .toc-level-1 a { color: var(--text-main); }
        .toc-level-2 a { font-size: 0.95em; }
        .toc-level-3 a { font-size: 0.9em; }
        .toc-level-4 a,
        .toc-level-5 a,
        .toc-level-6 a { font-size: 0.85em; color: var(--text-muted); }

        /* ============================================================
           Footnotes
           ============================================================ */

        .footnotes { margin-top: 4em; padding-top: 1em; }

        .footnotes-sep {
            margin-bottom: 1.5em;
            border-top: 2px solid var(--accent-soft) !important;
        }

        .footnotes-list {
            padding-left: 1.5em;
            color: var(--text-soft);
            font-size: 0.92em;
        }

        .footnote-item { margin: 0.8em 0; line-height: 1.6; }

        .footnote-number { color: var(--accent); font-weight: 600; margin-right: 0.3em; }

        .footnote-back {
            color: var(--accent);
            text-decoration: none;
            margin-left: 0.4em;
            opacity: 0.7;
            transition: opacity 0.2s ease;
        }

        .footnote-back:hover { opacity: 1; border-bottom: none; }

        .footnote-ref {
            font-size: 0.75em;
            line-height: 1;
            vertical-align: super;
        }

        .footnote-ref a {
            color: var(--accent);
            text-decoration: none;
            padding: 1px 3px;
            border-radius: 3px;
            transition: background 0.2s ease;
        }

        .footnote-ref a:hover { background: var(--accent-soft); border-bottom: none; }

        @media (max-width: 700px) {
            body { padding: 24px 16px 60px; }
            h1 { font-size: 1.7em; }
            .code-header { padding: 0.5em 0.7em; font-size: 0.75em; }
            .code-btn-label { display: none; }
            .code-btn { padding: 0.35em 0.5em; }
            .gallery-grid { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; gap: 10px; }
            .lightbox-stage { padding: 70px 16px 110px; }
            .lightbox-info { padding: 20px 20px 80px; }
            .lightbox-close, .lightbox-prev, .lightbox-next { width: 40px; height: 40px; }
            .lightbox-prev { left: 8px; }
            .lightbox-next { right: 8px; }
            .lightbox-close { top: 12px; right: 12px; }
            .lightbox-counter { top: 16px; }
            th, td { padding: 0.6em 0.7em; font-size: 0.88em; }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
            .reveal { opacity: 1 !important; transform: none !important; }
        }

        /* ============================================================
           RTL support
           ============================================================ */

        body.rtl {
            direction: rtl;
            text-align: right;
            font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif;
        }

        body.rtl ul, body.rtl ol { padding-left: 0; padding-right: 1.5em; }
        body.rtl ul.task-list, body.rtl ol.task-list { padding-right: 0; }

        body.rtl blockquote {
            border-left: none;
            border-right: 4px solid var(--accent);
            border-radius: 10px 0 0 10px;
        }

        body.rtl th, body.rtl td { text-align: right; }

        body.rtl h1, body.rtl h2, body.rtl h3,
        body.rtl h4, body.rtl h5, body.rtl h6,
        body.rtl p { text-align: right; }

        body.rtl .code-block,
        body.rtl pre,
        body.rtl code { direction: ltr; text-align: left; }

        body.rtl .code-header,
        body.rtl .code-header-left,
        body.rtl .code-buttons { direction: ltr; }

        body.rtl .code-block.rtl,
        body.rtl .code-block.rtl pre,
        body.rtl .code-block.rtl code { direction: rtl; text-align: right; }

        body.rtl .image-caption,
        body.rtl .image-description,
        body.rtl .gallery-caption { text-align: center; }

        body.rtl .lightbox { direction: ltr; }

        body.rtl .footnotes-list { padding-left: 0; padding-right: 1.5em; }
        body.rtl .footnote-back { margin-left: 0; margin-right: 0.4em; }
        body.rtl .toc-item { text-align: right; }
        body.rtl .toc-item[style*="padding-left"] { padding-left: 0 !important; }
        body.rtl .toc-item { padding-right: 0; }
    </style>
</head>
<body class="__BODY_CLASS__">
"""

TAIL = """
<!-- Lightbox -->
<div class="lightbox" id="mup-lightbox">
    <div class="lightbox-counter" id="mup-lightbox-counter">1 / 1</div>

    <button class="lightbox-close" onclick="mupCloseLightbox()" aria-label="Close">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"/>
            <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
    </button>

    <button class="lightbox-prev" onclick="mupPrevImage()" aria-label="Previous">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"/>
        </svg>
    </button>

    <button class="lightbox-next" onclick="mupNextImage()" aria-label="Next">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"/>
        </svg>
    </button>

    <div class="lightbox-stage" id="mup-lightbox-stage">
        <div class="lightbox-image-wrapper" id="mup-lightbox-wrapper">
            <img id="mup-lightbox-img" src="" alt="" onclick="mupToggleZoom()">
        </div>
    </div>

    <div class="lightbox-info" id="mup-lightbox-info">
        <div class="lightbox-caption" id="mup-lightbox-caption"></div>
        <div class="lightbox-description" id="mup-lightbox-description"></div>
    </div>

    <div class="lightbox-toolbar">
        <button class="lightbox-tool" onclick="mupZoomIn()" title="Zoom in">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                <line x1="11" y1="8" x2="11" y2="14"/>
                <line x1="8" y1="11" x2="14" y2="11"/>
            </svg>
        </button>
        <button class="lightbox-tool" onclick="mupZoomOut()" title="Zoom out">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                <line x1="8" y1="11" x2="14" y2="11"/>
            </svg>
        </button>
        <button class="lightbox-tool" onclick="mupResetZoom()" title="Reset">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                <path d="M3 3v5h5"/>
            </svg>
        </button>
        <button class="lightbox-tool" onclick="mupDownloadImage()" title="Download">
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
        </button>
    </div>
</div>

<script>
(function() {
    'use strict';

    function getCode(block) {
        var codeEl = block.querySelector('pre code');
        return codeEl ? codeEl.textContent : '';
    }

    function setSuccess(btn, label) {
        var labelEl = btn.querySelector('.code-btn-label');
        var original = labelEl ? labelEl.textContent : '';
        btn.classList.add('success');
        if (labelEl) labelEl.textContent = label;
        setTimeout(function() {
            btn.classList.remove('success');
            if (labelEl) labelEl.textContent = original;
        }, 1400);
    }

    function fallbackCopy(text) {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch(e) {}
        document.body.removeChild(ta);
    }

    function doCopy(block, btn) {
        var code = getCode(block);
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(code).then(function() {
                setSuccess(btn, 'Copied!');
            }).catch(function() {
                fallbackCopy(code);
                setSuccess(btn, 'Copied!');
            });
        } else {
            fallbackCopy(code);
            setSuccess(btn, 'Copied!');
        }
    }

    function doDownload(block, btn) {
        var code = getCode(block);
        var filename = btn.dataset.filename || 'code.txt';
        var blob = new Blob([code], { type: 'text/plain;charset=utf-8' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function() { URL.revokeObjectURL(url); }, 1000);
        setSuccess(btn, 'Saved!');
    }

    function doPreview(block, btn) {
        var preview = block.querySelector('.code-preview');
        var isOpen = !preview.hasAttribute('hidden');

        if (isOpen) {
            preview.setAttribute('hidden', '');
            preview.innerHTML = '';
            btn.classList.remove('active');
            return;
        }

        var code = block.dataset.previewCode || '';
        var lang = (block.dataset.previewLang || block.dataset.lang || 'html').toLowerCase();

        var textarea = document.createElement('textarea');
        textarea.innerHTML = code;
        code = textarea.value;

        preview.innerHTML = '';

        var doc = buildPreviewDoc(code, lang);

        if (lang === 'html' || lang === 'markup' || lang === 'css' || lang === 'javascript' || lang === 'js') {
            var iframe = document.createElement('iframe');
            iframe.setAttribute('sandbox', 'allow-scripts allow-modals');
            iframe.setAttribute('loading', 'lazy');
            iframe.srcdoc = doc;
            preview.appendChild(iframe);
        } else {
            preview.textContent = 'Preview not available for this language.';
        }

        preview.removeAttribute('hidden');
        btn.classList.add('active');
    }

    function buildPreviewDoc(code, lang) {
        var baseStyle = '<style>body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;padding:16px;margin:0;color:#222;background:#fff;line-height:1.6;}button{cursor:pointer;}</style>';

        if (lang === 'html' || lang === 'markup') {
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' +
                   baseStyle + '</head><body>' + code + '</body></html>';
        }

        if (lang === 'css') {
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' +
                   baseStyle +
                   '<style>' + code + '</style></head><body>' +
                   '<h1>Heading 1</h1>' +
                   '<p>This is a sample paragraph to preview your CSS.</p>' +
                   '<button>Sample Button</button>' +
                   '</body></html>';
        }

        if (lang === 'javascript' || lang === 'js') {
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' +
                   baseStyle +
                   '<style>#mup-out{font-family:monospace;font-size:14px;background:#f5f5f5;padding:12px;border-radius:6px;min-height:60px;white-space:pre-wrap;}</style>' +
                   '</head><body>' +
                   '<div id="mup-out"></div>' +
                   '<script>' +
                   'var out=document.getElementById("mup-out");' +
                   'var log=console.log;' +
                   'console.log=function(){' +
                   '  var line=Array.prototype.slice.call(arguments).map(function(x){' +
                   '    return typeof x==="object"?JSON.stringify(x,null,2):String(x);' +
                   '  }).join(" ");' +
                   '  out.textContent+=line+"\\n";' +
                   '  log.apply(console,arguments);' +
                   '};' +
                   'window.onerror=function(m){out.textContent+="Error: "+m+"\\n";};' +
                   'try{' + code + '}catch(e){out.textContent+="Error: "+e.message;}' +
                   '<\\/script></body></html>';
        }

        return '<!DOCTYPE html><html><body><p>Preview not available.</p></body></html>';
    }

    var mupLightboxImages = [];
    var mupLightboxIndex = 0;
    var mupZoomLevel = 1;

    function mupOpenLightbox(images, startIndex) {
        mupLightboxImages = images;
        mupLightboxIndex = startIndex;
        mupZoomLevel = 1;

        var lb = document.getElementById('mup-lightbox');
        if (!lb) return;

        mupUpdateLightbox();
        lb.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function mupUpdateLightbox() {
        var img = document.getElementById('mup-lightbox-img');
        var cap = document.getElementById('mup-lightbox-caption');
        var desc = document.getElementById('mup-lightbox-description');
        var counter = document.getElementById('mup-lightbox-counter');
        var wrapper = document.getElementById('mup-lightbox-wrapper');

        if (!img || !mupLightboxImages.length) return;

        mupZoomLevel = 1;
        if (wrapper) wrapper.classList.remove('zoomed');
        img.style.transform = '';

        var current = mupLightboxImages[mupLightboxIndex];

        img.style.opacity = '0';
        setTimeout(function() {
            img.src = current.src;
            img.alt = current.caption || '';
            if (cap) cap.textContent = current.caption || '';
            if (desc) desc.textContent = current.description || '';
            if (counter) counter.textContent = (mupLightboxIndex + 1) + ' / ' + mupLightboxImages.length;
            img.style.opacity = '1';
        }, 120);
    }

    function mupCloseLightbox() {
        var lb = document.getElementById('mup-lightbox');
        if (lb) lb.classList.remove('active');
        document.body.style.overflow = '';
    }

    function mupNextImage() {
        if (!mupLightboxImages.length) return;
        mupLightboxIndex = (mupLightboxIndex + 1) % mupLightboxImages.length;
        mupUpdateLightbox();
    }

    function mupPrevImage() {
        if (!mupLightboxImages.length) return;
        mupLightboxIndex = (mupLightboxIndex - 1 + mupLightboxImages.length) % mupLightboxImages.length;
        mupUpdateLightbox();
    }

    function mupToggleZoom() {
        mupZoomLevel = mupZoomLevel > 1 ? 1 : 2;
        mupApplyZoom();
    }

    function mupZoomIn() {
        mupZoomLevel = Math.min(mupZoomLevel + 0.5, 4);
        mupApplyZoom();
    }

    function mupZoomOut() {
        mupZoomLevel = Math.max(mupZoomLevel - 0.5, 1);
        mupApplyZoom();
    }

    function mupResetZoom() {
        mupZoomLevel = 1;
        mupApplyZoom();
    }

    function mupApplyZoom() {
        var img = document.getElementById('mup-lightbox-img');
        var wrapper = document.getElementById('mup-lightbox-wrapper');
        if (!img || !wrapper) return;

        if (mupZoomLevel > 1) {
            wrapper.classList.add('zoomed');
            img.style.transform = 'scale(' + mupZoomLevel + ')';
        } else {
            wrapper.classList.remove('zoomed');
            img.style.transform = '';
        }
    }

    function mupDownloadImage() {
        var current = mupLightboxImages[mupLightboxIndex];
        if (!current || !current.src) return;

        var url = current.src;
        var caption = (current.caption || 'image').trim();
        var baseName = caption
            .replace(/[^\\w\\u0600-\\u06FF\\-]+/g, '-')
            .replace(/^-+|-+$/g, '')
            .substring(0, 60) || 'image';

        var ext = 'jpg';
        var m = url.match(/\\.(jpg|jpeg|png|gif|webp|avif|svg|bmp)(\\?|#|$)/i);
        if (m) ext = m[1].toLowerCase();

        var filename = baseName + '.' + ext;

        var btns = document.querySelectorAll('.lightbox-tool');
        var dlBtn = btns[btns.length - 1];

        fetch(url, { mode: 'cors' })
            .then(function(resp) {
                if (!resp.ok) throw new Error('fetch failed');
                return resp.blob();
            })
            .then(function(blob) {
                var objectUrl = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = objectUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                setTimeout(function() { URL.revokeObjectURL(objectUrl); }, 1000);
                flashSuccess(dlBtn);
            })
            .catch(function() {
                var a = document.createElement('a');
                a.href = url;
                a.download = filename;
                a.target = '_blank';
                a.rel = 'noopener noreferrer';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                flashSuccess(dlBtn);
            });
    }

    function flashSuccess(btn) {
        if (!btn) return;
        btn.style.background = 'rgba(16, 185, 129, 0.35)';
        btn.style.color = '#10b981';
        setTimeout(function() {
            btn.style.background = '';
            btn.style.color = '';
        }, 800);
    }

    window.mupCloseLightbox = mupCloseLightbox;
    window.mupNextImage = mupNextImage;
    window.mupPrevImage = mupPrevImage;
    window.mupToggleZoom = mupToggleZoom;
    window.mupZoomIn = mupZoomIn;
    window.mupZoomOut = mupZoomOut;
    window.mupResetZoom = mupResetZoom;
    window.mupDownloadImage = mupDownloadImage;

    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.code-btn');
        if (btn) {
            var block = btn.closest('.code-block');
            if (!block) return;
            var action = btn.dataset.action;
            if (action === 'copy') {
                doCopy(block, btn);
            } else if (action === 'download') {
                doDownload(block, btn);
            } else if (action === 'preview') {
                doPreview(block, btn);
            }
            return;
        }

        var item = e.target.closest('.gallery-item');
        if (item) {
            var gallery = item.closest('.gallery');
            var allItems = gallery.querySelectorAll('.gallery-item');
            var images = [];
            allItems.forEach(function(el) {
                images.push({
                    src: el.dataset.src,
                    caption: el.dataset.caption,
                    description: el.dataset.description || ''
                });
            });
            var idx = parseInt(item.dataset.index, 10) || 0;
            mupOpenLightbox(images, idx);
            return;
        }

        var single = e.target.closest('.image-single');
        if (single) {
            var images = [{
                src: single.dataset.src,
                caption: single.dataset.caption,
                description: single.dataset.description || ''
            }];
            mupOpenLightbox(images, 0);
            return;
        }

        var lb = document.getElementById('mup-lightbox');
        if (lb && lb.classList.contains('active')) {
            var wrapper = e.target.closest('.lightbox-image-wrapper');
            var lbBtn = e.target.closest('.lightbox-close, .lightbox-prev, .lightbox-next, .lightbox-tool');
            if (!wrapper && !lbBtn) {
                mupCloseLightbox();
            }
        }
    });

    document.addEventListener('keydown', function(e) {
        var lb = document.getElementById('mup-lightbox');
        if (!lb || !lb.classList.contains('active')) return;

        if (e.key === 'Escape') {
            mupCloseLightbox();
        } else if (e.key === 'ArrowRight') {
            mupNextImage();
        } else if (e.key === 'ArrowLeft') {
            mupPrevImage();
        } else if (e.key === '+' || e.key === '=') {
            mupZoomIn();
        } else if (e.key === '-') {
            mupZoomOut();
        } else if (e.key === '0') {
            mupResetZoom();
        }
    });

    var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    var prismLink = document.getElementById('prism-theme');
    if (prismLink) {
        prismLink.href = currentTheme === 'light'
            ? 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css'
            : 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css';
    }

    function initScrollReveal() {
        var elements = document.querySelectorAll('.reveal');

        if (!('IntersectionObserver' in window)) {
            elements.forEach(function(el) { el.classList.add('visible'); });
            return;
        }

        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -60px 0px'
        });

        elements.forEach(function(el) {
            observer.observe(el);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollReveal);
    } else {
        initScrollReveal();
    }
})();
</script>
</body>
</html>
"""


# ============================================================
# Public API
# ============================================================

def to_html(
    text: str,
    title: str = "Markup+ Document",
    theme: str = "light",
    direction: str = None,
) -> str:
    """
    Convert Markup+ source text to a complete HTML page.

    Args:
        text:       Markup+ source text.
        title:      HTML page title.
        theme:      "light" (default) or "dark".
        direction:  "ltr", "rtl", or None (auto-detect from content).
    """
    from .parser import parse_text

    doc = parse_text(text)

    meta = dict(doc.meta) if doc.meta else {}
    if meta.get("title"):
        title = meta["title"]

    body = render_ast(doc)

    theme = theme if theme in ("light", "dark") else "light"

    if direction in ("ltr", "rtl"):
        final_dir = direction
    else:
        combined = title + " " + text
        final_dir = "rtl" if is_rtl_text(combined) else "ltr"

    lang_code = "fa" if final_dir == "rtl" else "en"

    head = HEAD.replace("__TITLE__", html.escape(title))
    head = head.replace("__THEME__", theme)
    head = head.replace("__DIR__", final_dir)
    head = head.replace("__LANG__", lang_code)
    head = head.replace("__BODY_CLASS__", final_dir)

    return head + body + TAIL
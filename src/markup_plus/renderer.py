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
    - Phase 5: Components, Charts, Math, Tabs, Collapse, Alerts, Quotes, Timeline
    - Native-like smooth animations
    - Scroll reveal animations
    - External CSS themes (via themes module)
"""

import html
import re
import json
import unicodedata
import operator as _op
from typing import Any, List

from .ast import (
    AlertBlock,
    BlockQuote,
    ChartBlock,
    CodeBlock,
    CollapseBlock,
    ComponentCall,
    ComponentDef,
    Document,
    EachBlock,
    GalleryBlock,
    Heading,
    HorizontalRule,
    IfBlock,
    ImageBlock,
    ImportBlock,
    ListBlock,
    MathBlock,
    Paragraph,
    QuoteBlock,
    TableBlock,
    TabsBlock,
    TimelineBlock,
    TOCBlock,
    VariableDef,
    Node,
)
from .themes import build_css


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
RE_MATH_INLINE = re.compile(r"\$([^\$\n]+?)\$")


def render_inline(text: str) -> str:
    """Render inline formatting inside a text string."""
    autolinks = []

    def stash_autolink(m):
        idx = len(autolinks)
        autolinks.append(m.group(1))
        return f"\x00AUTOLINK{idx}\x00"

    text = RE_AUTOLINK.sub(stash_autolink, text)

    math_items = []

    def stash_math(m):
        idx = len(math_items)
        math_items.append(m.group(1))
        return f"\x00INLINEMATH{idx}\x00"

    text = RE_MATH_INLINE.sub(stash_math, text)

    text = html.escape(text, quote=False)

    text = RE_CODE_INLINE.sub(r"<code>\1</code>", text)
    text = RE_STRIKE.sub(r"<del>\1</del>", text)
    text = RE_BOLD.sub(r"<strong>\1</strong>", text)
    text = RE_ITALIC.sub(r"<em>\1</em>", text)

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

    for idx, url in enumerate(autolinks):
        url_escaped = html.escape(url, quote=True)
        replacement = (
            f'<a href="{url_escaped}" '
            f'target="_blank" rel="noopener noreferrer">{url}</a>'
        )
        text = text.replace(f"\x00AUTOLINK{idx}\x00", replacement)

    for idx, latex in enumerate(math_items):
        latex_escaped = html.escape(latex, quote=False)
        replacement = f'<span class="math-inline">${latex_escaped}$</span>'
        text = text.replace(f"\x00INLINEMATH{idx}\x00", replacement)

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
# Phase 5: Rich feature renderers
# ============================================================

ALERT_ICONS = {
    "note": "ℹ️",
    "warning": "⚠️",
    "tip": "💡",
    "danger": "🚨",
    "success": "✅",
}

ALERT_TITLES = {
    "note": "Note",
    "warning": "Warning",
    "tip": "Tip",
    "danger": "Danger",
    "success": "Success",
}


def render_component_def(node: ComponentDef, doc: Document, context: dict) -> str:
    """Component definitions don't render."""
    return ""


def render_component_call(node: ComponentCall, doc: Document, context: dict) -> str:
    """Render a component call by looking up its definition."""
    if doc is not None and not hasattr(doc, "_components"):
        doc._components = {}

        def collect(children):
            for child in children:
                if isinstance(child, ComponentDef):
                    doc._components[child.name] = child
                elif isinstance(child, IfBlock):
                    for _, bc in child.branches:
                        collect(bc)
                elif isinstance(child, EachBlock):
                    collect(child.children)

        collect(doc.children)

    comp_def = doc._components.get(node.name) if doc else None
    if not comp_def:
        return f'<p class="component-missing">[Component not found: {node.name}]</p>'

    child_ctx = dict(context)
    for k, v in node.args.items():
        child_ctx[k] = v

    return _render_children(comp_def.children, doc, child_ctx)


def render_chart(node: ChartBlock, context: dict) -> str:
    """Render a chart with Chart.js."""
    chart_id = f"mup-chart-{id(node) % 1000000}"
    chart_type = node.chart_type or "bar"
    data_json = json.dumps(node.data)
    labels_json = json.dumps(node.labels)
    title = substitute_variables(node.title, context) if node.title else ""

    title_html = ""
    if title:
        title_html = f'<div class="chart-title">{html.escape(title)}</div>'

    return (
        f'<div class="chart-block reveal">'
        f"{title_html}"
        f'<div class="chart-canvas-wrapper">'
        f'<canvas id="{chart_id}"></canvas>'
        f"</div>"
        f'<script type="application/json" class="chart-data">'
        f'{{"id": "{chart_id}", "type": "{chart_type}", "data": {data_json}, "labels": {labels_json}}}'
        f"</script>"
        f"</div>"
    )


def render_math(node: MathBlock, context: dict = None) -> str:
    """Render a math block with KaTeX."""
    latex = html.escape(node.latex, quote=False)
    if node.display:
        return f'<div class="math-block reveal">$${latex}$$</div>'
    else:
        return f'<span class="math-inline">${latex}$</span>'


def render_tabs(node: TabsBlock, doc: Document, context: dict) -> str:
    """Render a tabs block."""
    if not node.tabs:
        return ""

    tabs_id = f"mup-tabs-{id(node) % 1000000}"

    buttons = []
    for i, (title, _) in enumerate(node.tabs):
        active = " active" if i == 0 else ""
        title_sub = substitute_variables(title, context)
        buttons.append(
            f'<button class="tab-button{active}" data-tab-index="{i}" '
            f'data-tab-group="{tabs_id}">{html.escape(title_sub)}</button>'
        )

    panels = []
    for i, (title, children) in enumerate(node.tabs):
        active = " active" if i == 0 else ""
        content = _render_children(children, doc, context)
        panels.append(
            f'<div class="tab-panel{active}" data-tab-index="{i}" '
            f'data-tab-group="{tabs_id}">{content}</div>'
        )

    return (
        f'<div class="tabs-block reveal" data-tabs-id="{tabs_id}">'
        f'<div class="tabs-header">{"".join(buttons)}</div>'
        f'<div class="tabs-content">{"".join(panels)}</div>'
        f"</div>"
    )


def render_collapse(node: CollapseBlock, doc: Document, context: dict) -> str:
    """Render a collapse/accordion block."""
    if not node.items:
        return ""

    items_html = []
    for title, children in node.items:
        title_sub = substitute_variables(title, context)
        content = _render_children(children, doc, context)
        items_html.append(
            f'<div class="collapse-item">'
            f'<button class="collapse-header">'
            f'<span class="collapse-title">{html.escape(title_sub)}</span>'
            f'<span class="collapse-icon">▼</span>'
            f"</button>"
            f'<div class="collapse-body">{content}</div>'
            f"</div>"
        )

    return f'<div class="collapse-block reveal">{"".join(items_html)}</div>'


def render_alert(node: AlertBlock, doc: Document, context: dict) -> str:
    """Render an alert box."""
    alert_type = node.alert_type or "note"
    icon = ALERT_ICONS.get(alert_type, "ℹ️")
    title = ALERT_TITLES.get(alert_type, alert_type.title())
    content = _render_children(node.children, doc, context)

    return (
        f'<div class="alert-block alert-{alert_type} reveal">'
        f'<div class="alert-header">'
        f'<span class="alert-icon">{icon}</span>'
        f'<span class="alert-title">{title}</span>'
        f"</div>"
        f'<div class="alert-content">{content}</div>'
        f"</div>"
    )


def render_quote(node: QuoteBlock, context: dict) -> str:
    """Render a rich quote with author/source."""
    text = substitute_variables(node.text, context)
    author = substitute_variables(node.author, context) if node.author else ""
    source = substitute_variables(node.source, context) if node.source else ""

    text_html = render_inline(text.replace("\n", " "))

    footer = ""
    if author or source:
        parts = []
        if author:
            parts.append(html.escape(author))
        if source:
            parts.append(f"<cite>{html.escape(source)}</cite>")
        footer = f'<footer class="quote-footer">— {" ، ".join(parts)}</footer>'

    return (
        f'<blockquote class="rich-quote reveal">'
        f'<div class="quote-text">{text_html}</div>'
        f"{footer}"
        f"</blockquote>"
    )


def render_timeline(node: TimelineBlock, context: dict) -> str:
    """Render a timeline."""
    if not node.events:
        return ""

    items = []
    for date, text in node.events:
        text_sub = substitute_variables(text, context)
        items.append(
            f'<div class="timeline-item">'
            f'<div class="timeline-dot"></div>'
            f'<div class="timeline-date">{html.escape(date)}</div>'
            f'<div class="timeline-text">{render_inline(text_sub)}</div>'
            f"</div>"
        )

    return f'<div class="timeline-block reveal">{"".join(items)}</div>'


# ============================================================
# Block rendering (with context)
# ============================================================

def render_node(node: Node, doc: Document = None, context: dict = None) -> str:
    """Render a single node with optional context."""
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

    if isinstance(node, ComponentDef):
        return render_component_def(node, doc, context)

    if isinstance(node, ComponentCall):
        return render_component_call(node, doc, context)

    if isinstance(node, ChartBlock):
        return render_chart(node, context)

    if isinstance(node, MathBlock):
        return render_math(node, context)

    if isinstance(node, TabsBlock):
        return render_tabs(node, doc, context)

    if isinstance(node, CollapseBlock):
        return render_collapse(node, doc, context)

    if isinstance(node, AlertBlock):
        return render_alert(node, doc, context)

    if isinstance(node, QuoteBlock):
        return render_quote(node, context)

    if isinstance(node, TimelineBlock):
        return render_timeline(node, context)

    if isinstance(node, ImportBlock):
        return ""

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
    context = dict(doc.meta) if doc.meta else {}
    context.update(doc.variables)

    parts = []
    for child in doc.children:
        rendered = render_node(child, doc, context)
        if rendered:
            parts.append(rendered)

    body = "\n".join(parts)

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

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

    <!-- KaTeX -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

    <style>
__CSS__
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
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' + baseStyle + '</head><body>' + code + '</body></html>';
        }

        if (lang === 'css') {
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' + baseStyle +
                   '<style>' + code + '</style></head><body>' +
                   '<h1>Heading 1</h1><p>This is a sample paragraph to preview your CSS.</p><button>Sample Button</button>' +
                   '</body></html>';
        }

        if (lang === 'javascript' || lang === 'js') {
            return '<!DOCTYPE html><html><head><meta charset="utf-8">' + baseStyle +
                   '<style>#mup-out{font-family:monospace;font-size:14px;background:#f5f5f5;padding:12px;border-radius:6px;min-height:60px;white-space:pre-wrap;}</style>' +
                   '</head><body><div id="mup-out"></div><script>' +
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
            if (action === 'copy') doCopy(block, btn);
            else if (action === 'download') doDownload(block, btn);
            else if (action === 'preview') doPreview(block, btn);
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
            if (!wrapper && !lbBtn) mupCloseLightbox();
        }
    });

    document.addEventListener('keydown', function(e) {
        var lb = document.getElementById('mup-lightbox');
        if (!lb || !lb.classList.contains('active')) return;

        if (e.key === 'Escape') mupCloseLightbox();
        else if (e.key === 'ArrowRight') mupNextImage();
        else if (e.key === 'ArrowLeft') mupPrevImage();
        else if (e.key === '+' || e.key === '=') mupZoomIn();
        else if (e.key === '-') mupZoomOut();
        else if (e.key === '0') mupResetZoom();
    });

    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.tab-button');
        if (btn) {
            var group = btn.dataset.tabGroup;
            var idx = btn.dataset.tabIndex;

            document.querySelectorAll('.tab-button[data-tab-group="' + group + '"]').forEach(function(b) {
                b.classList.remove('active');
            });
            document.querySelectorAll('.tab-panel[data-tab-group="' + group + '"]').forEach(function(p) {
                p.classList.remove('active');
            });

            btn.classList.add('active');
            var panel = document.querySelector('.tab-panel[data-tab-group="' + group + '"][data-tab-index="' + idx + '"]');
            if (panel) panel.classList.add('active');
        }
    });

    document.addEventListener('click', function(e) {
        var header = e.target.closest('.collapse-header');
        if (header) {
            var item = header.closest('.collapse-item');
            if (item) item.classList.toggle('open');
        }
    });

    function initCharts() {
        if (typeof Chart === 'undefined') return;

        document.querySelectorAll('.chart-data').forEach(function(script) {
            try {
                var cfg = JSON.parse(script.textContent);
                var canvas = document.getElementById(cfg.id);
                if (!canvas) return;

                var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
                var textColor = isDark ? '#e4e4e7' : '#333';
                var gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

                new Chart(canvas.getContext('2d'), {
                    type: cfg.type,
                    data: {
                        labels: cfg.labels,
                        datasets: [{
                            data: cfg.data,
                            backgroundColor: [
                                'rgba(124, 58, 237, 0.7)',
                                'rgba(236, 72, 153, 0.7)',
                                'rgba(59, 130, 246, 0.7)',
                                'rgba(16, 185, 129, 0.7)',
                                'rgba(251, 191, 36, 0.7)',
                                'rgba(239, 68, 68, 0.7)'
                            ],
                            borderColor: 'rgba(124, 58, 237, 1)',
                            borderWidth: 2,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: cfg.type === 'pie' || cfg.type === 'doughnut',
                                labels: { color: textColor }
                            }
                        },
                        scales: (cfg.type === 'pie' || cfg.type === 'doughnut') ? {} : {
                            y: {
                                beginAtZero: true,
                                ticks: { color: textColor },
                                grid: { color: gridColor }
                            },
                            x: {
                                ticks: { color: textColor },
                                grid: { color: gridColor }
                            }
                        }
                    }
                });
            } catch (err) {
                console.error('Chart error:', err);
            }
        });
    }

    function initMath() {
        if (typeof renderMathInElement === 'undefined') return;
        try {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false}
                ],
                throwOnError: false
            });
        } catch (err) {
            console.error('KaTeX error:', err);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            initMath();
        });
    } else {
        initCharts();
        initMath();
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
# Import resolution (Phase 6 / v0.6.0)
# ============================================================

def resolve_imports(doc: Document, base_dir: str = None) -> None:
    """
    Resolve @import directives by loading and parsing external files.

    Modifies the document in-place, replacing ImportBlock nodes with
    the parsed children of the imported file.
    """
    import os
    from pathlib import Path
    from .parser import parse_text as _parse_text

    if base_dir is None:
        base_dir = os.getcwd()

    base_path = Path(base_dir)
    seen_files = set()

    def load_import(import_node: ImportBlock, current_dir: Path) -> list:
        target = (current_dir / import_node.path).resolve()

        if str(target) in seen_files:
            return [Paragraph(
                text=f"[Circular import: {import_node.path}]",
                line=import_node.line,
            )]

        if not target.exists():
            return [Paragraph(
                text=f"[Import not found: {import_node.path}]",
                line=import_node.line,
            )]

        try:
            seen_files.add(str(target))
            source = target.read_text(encoding="utf-8")
            sub_doc = _parse_text(source)
            resolve_imports(sub_doc, base_dir=str(target.parent))
            return sub_doc.children
        except Exception as e:
            return [Paragraph(
                text=f"[Import error: {import_node.path} — {e}]",
                line=import_node.line,
            )]

    def process_children(children: list, current_dir: Path) -> list:
        result = []
        for child in children:
            if isinstance(child, ImportBlock):
                imported = load_import(child, current_dir)
                result.extend(process_children(imported, current_dir))
            elif isinstance(child, IfBlock):
                new_branches = []
                for condition, branch_children in child.branches:
                    new_children = process_children(branch_children, current_dir)
                    new_branches.append((condition, new_children))
                child.branches = new_branches
                result.append(child)
            elif isinstance(child, EachBlock):
                child.children = process_children(child.children, current_dir)
                result.append(child)
            elif isinstance(child, ComponentDef):
                child.children = process_children(child.children, current_dir)
                result.append(child)
            elif isinstance(child, (TabsBlock, CollapseBlock, AlertBlock)):
                if hasattr(child, "children") and child.children:
                    child.children = process_children(child.children, current_dir)
                result.append(child)
            else:
                result.append(child)
        return result

    doc.children = process_children(doc.children, base_path)


# ============================================================
# Public API
# ============================================================

def to_html(
    text: str,
    title: str = "Markup+ Document",
    theme: str = "light",
    direction: str = None,
    base_dir: str = None,
    custom_css: str = None,
) -> str:
    """Convert Markup+ source text to a complete HTML page."""
    from .parser import parse_text

    doc = parse_text(text)

    # Resolve @import directives
    resolve_imports(doc, base_dir=base_dir)

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

    # Build CSS (base + optional custom)
    css_content = build_css(custom_css)

    head = HEAD.replace("__TITLE__", html.escape(title))
    head = head.replace("__THEME__", theme)
    head = head.replace("__DIR__", final_dir)
    head = head.replace("__LANG__", lang_code)
    head = head.replace("__BODY_CLASS__", final_dir)
    head = head.replace("__CSS__", css_content)

    return head + body + TAIL
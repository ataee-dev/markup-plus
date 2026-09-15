"""
Markup+ Renderer

Converts an AST Document into HTML output.

Features:
    - Light + Dark themes (CLI: --dark / --light)
    - Headings, paragraphs, lists, blockquotes, HR
    - Enhanced code blocks with copy/download/preview
    - Images with lightbox, zoom, and description
    - Galleries with lightbox, keyboard nav, zoom toolbar
    - Native-like smooth animations
    - Scroll reveal animations
"""

import html
import re

from .ast import (
    BlockQuote,
    CodeBlock,
    Document,
    GalleryBlock,
    Heading,
    HorizontalRule,
    ImageBlock,
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

    # RTL languages
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

    # No line numbers — clean display
    code_html = code_escaped

    wrap_class = " wrap" if node.wrap else ""
    previewable_class = " previewable" if previewable else ""
    rtl_class = " rtl" if is_rtl else ""

    # Store preview code for HTML/CSS/JS blocks
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
        f'<pre><code class="language-{lang}">{code_html}</code></pre>'
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
# Block rendering
# ============================================================

def render_node(node: Node) -> str:
    if isinstance(node, Heading):
        level = max(1, min(node.level, 6))
        return f'<h{level} class="reveal">{render_inline(node.text)}</h{level}>'

    if isinstance(node, Paragraph):
        return f'<p class="reveal">{render_inline(node.text)}</p>'

    if isinstance(node, ListBlock):
        tag = "ol" if node.ordered else "ul"
        items_html = "\n".join(
            f"  <li>{render_inline(item)}</li>" for item in node.items
        )
        return f'<{tag} class="reveal">\n{items_html}\n</{tag}>'

    if isinstance(node, BlockQuote):
        lines = node.text.split("\n")
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

    return ""


def render_ast(doc: Document) -> str:
    parts = [render_node(child) for child in doc.children]
    return "\n".join(p for p in parts if p)


# ============================================================
# HTML Template
# ============================================================

HEAD = """<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="__THEME__">
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
        /* ============================================================
           Theme variables
           ============================================================ */

        :root,
        [data-theme="light"] {
            --bg-page: #ffffff;
            --bg-soft: #f4f4f5;
            --bg-code: #f6f8fa;
            --bg-code-header: #eaedf0;
            --bg-blockquote: #f8f5ff;
            --bg-preview: #fafafa;

            --text-main: #18181b;
            --text-soft: #52525b;
            --text-muted: #71717a;

            --border: #e4e4e7;
            --border-code: #d0d7de;

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

            --text-main: #e4e4e7;
            --text-soft: #d4d4d8;
            --text-muted: #a1a1aa;

            --border: rgba(255, 255, 255, 0.1);
            --border-code: rgba(255, 255, 255, 0.06);

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

        /* ============================================================
           Reset & base
           ============================================================ */

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

        /* ============================================================
           Typography
           ============================================================ */

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
            transition: color 0.2s ease;
        }

        a:hover { color: var(--accent-hover); }

        /* ============================================================
           Scroll reveal animation
           ============================================================ */

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

        /* Stagger children inside galleries */
        .gallery-grid .reveal:nth-child(1) { transition-delay: 0.00s; }
        .gallery-grid .reveal:nth-child(2) { transition-delay: 0.06s; }
        .gallery-grid .reveal:nth-child(3) { transition-delay: 0.12s; }
        .gallery-grid .reveal:nth-child(4) { transition-delay: 0.18s; }
        .gallery-grid .reveal:nth-child(5) { transition-delay: 0.24s; }
        .gallery-grid .reveal:nth-child(6) { transition-delay: 0.30s; }
        .gallery-grid .reveal:nth-child(7) { transition-delay: 0.36s; }
        .gallery-grid .reveal:nth-child(8) { transition-delay: 0.42s; }
        .gallery-grid .reveal:nth-child(n+9) { transition-delay: 0.48s; }

        /* ============================================================
           Single Image
           ============================================================ */

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

        .image-single:hover .image-single-overlay {
            opacity: 1;
        }

        .image-single-static { display: inline-block; max-width: 100%; }
        .image-single-static img {
            display: block;
            max-width: 100%;
            height: auto;
            border-radius: 12px;
        }

        .image-align-center {
            display: flex;
            justify-content: center;
            margin: 1.5em 0;
        }

        .image-align-left {
            display: flex;
            justify-content: flex-start;
            margin: 1.5em 0;
        }

        .image-align-right {
            display: flex;
            justify-content: flex-end;
            margin: 1.5em 0;
        }

        .image-figure {
            margin: 1.5em 0;
            display: inline-block;
            text-align: center;
            max-width: 100%;
        }

        .image-figure .image-single,
        .image-figure .image-single-static {
            display: inline-block;
        }

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

        /* ============================================================
           Code blocks
           ============================================================ */

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
            transition:
                background 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                color 0.25s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
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

        /* RTL code */
        .code-block.rtl pre {
            direction: rtl;
        }

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

        /* ============================================================
           Gallery
           ============================================================ */

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

        /* ============================================================
           Lightbox
           ============================================================ */

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

        .lightbox.active {
            display: flex;
            opacity: 1;
        }

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

        .lightbox-image-wrapper.zoomed {
            max-width: none;
            max-height: none;
            transform: scale(1);
        }

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
            transition:
                opacity 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 10001;
        }

        .lightbox.active .lightbox-info {
            opacity: 1;
            transform: translateY(0);
            transition-delay: 0.15s;
        }

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
            transition:
                opacity 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .lightbox.active .lightbox-counter {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
            transition-delay: 0.1s;
        }

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
            transition:
                opacity 0.45s cubic-bezier(0.4, 0, 0.2, 1),
                transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .lightbox.active .lightbox-toolbar {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
            transition-delay: 0.2s;
        }

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

        .lightbox-tool:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: scale(1.1);
        }

        .lightbox-tool:active { transform: scale(0.92); }

        /* ============================================================
           Responsive
           ============================================================ */

        @media (max-width: 700px) {
            body { padding: 24px 16px 60px; }
            h1 { font-size: 1.7em; }

            .code-header { padding: 0.5em 0.7em; font-size: 0.75em; }
            .code-btn-label { display: none; }
            .code-btn { padding: 0.35em 0.5em; }

            .gallery-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 10px;
            }

            .lightbox-stage { padding: 70px 16px 110px; }
            .lightbox-info { padding: 20px 20px 80px; }
            .lightbox-close,
            .lightbox-prev,
            .lightbox-next {
                width: 40px;
                height: 40px;
            }
            .lightbox-prev { left: 8px; }
            .lightbox-next { right: 8px; }
            .lightbox-close { top: 12px; right: 12px; }
            .lightbox-counter { top: 16px; }
        }

        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
            .reveal {
                opacity: 1 !important;
                transform: none !important;
            }
        }
    </style>
</head>
<body>
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

    // ============================================================
    // Code block helpers
    // ============================================================

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

        // Unescape HTML entities
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

    // ============================================================
    // Lightbox
    // ============================================================

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
            .replace(/[^\w\u0600-\u06FF\-]+/g, '-')
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

    // Expose to global
    window.mupCloseLightbox = mupCloseLightbox;
    window.mupNextImage = mupNextImage;
    window.mupPrevImage = mupPrevImage;
    window.mupToggleZoom = mupToggleZoom;
    window.mupZoomIn = mupZoomIn;
    window.mupZoomOut = mupZoomOut;
    window.mupResetZoom = mupResetZoom;
    window.mupDownloadImage = mupDownloadImage;

    // ============================================================
    // Event delegation
    // ============================================================

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

    // ============================================================
    // Prism theme auto-switch on theme
    // ============================================================

    var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    var prismLink = document.getElementById('prism-theme');
    if (prismLink) {
        prismLink.href = currentTheme === 'light'
            ? 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism.min.css'
            : 'https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css';
    }

    // ============================================================
    // Scroll reveal (IntersectionObserver)
    // ============================================================

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


def to_html(text: str, title: str = "Markup+ Document", theme: str = "light") -> str:
    """
    Convert Markup+ source text to a complete HTML page.

    Args:
        text:   Markup+ source text.
        title:  HTML page title.
        theme:  "light" (default) or "dark".
    """
    from .parser import parse_text

    doc = parse_text(text)
    body = render_ast(doc)

    theme = theme if theme in ("light", "dark") else "light"

    head = HEAD.replace("__TITLE__", html.escape(title))
    head = head.replace("__THEME__", theme)

    return head + body + TAIL
"""
Markup+ Renderer

Converts an AST Document into HTML output.
"""

import html
import re

from .ast import (
    BlockQuote,
    CodeBlock,
    Document,
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

    if node.linenos:
        lines = node.code.split("\n")
        lines_html = []
        for i, line in enumerate(lines, start=1):
            line_escaped = html.escape(line, quote=False)
            hl_class = " hl" if i in node.highlight else ""
            lines_html.append(
                f'<span class="code-line{hl_class}">'
                f'<span class="line-num">{i}</span>'
                f'<span class="line-content">{line_escaped}</span>'
                f"</span>"
            )
        code_html = "\n".join(lines_html)
    else:
        code_html = code_escaped

    wrap_class = " wrap" if node.wrap else ""
    previewable_class = " previewable" if previewable else ""

    return (
        f'<div class="code-block{wrap_class}{previewable_class}" '
        f'data-lang="{lang}">'
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
    """Render an image with optional options."""
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

    style = "max-width: 100%; height: auto; border-radius: 8px;"
    img = f'<img {" ".join(attrs)} style="{style}">'

    if node.link:
        img = (
            f'<a href="{html.escape(node.link, quote=True)}" '
            f'target="_blank" rel="noopener noreferrer">{img}</a>'
        )

    if node.caption:
        inner = (
            f'<figure class="image-figure">'
            f"{img}"
            f'<figcaption>{render_inline(node.caption)}</figcaption>'
            f"</figure>"
        )
    else:
        inner = img

    align = (node.align or "").lower()
    if align in ("center", "left", "right"):
        return f'<div class="image-align-{align}">{inner}</div>'

    return inner


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
        lines = node.text.split("\n")
        inner = "\n".join(f"<p>{render_inline(line)}</p>" for line in lines)
        return f"<blockquote>\n{inner}\n</blockquote>"

    if isinstance(node, HorizontalRule):
        return "<hr>"

    if isinstance(node, CodeBlock):
        return render_code_block(node)

    if isinstance(node, ImageBlock):
        return render_image(node)

    return ""


def render_ast(doc: Document) -> str:
    parts = [render_node(child) for child in doc.children]
    return "\n".join(p for p in parts if p)


# ============================================================
# HTML Template — Dark only
# ============================================================

HEAD = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>

    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/prism-tomorrow.min.css">
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/prism.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-javascript.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-json.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-markup.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-css.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs@1.29.0/components/prism-typescript.min.js"></script>

    <style>
        * { box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.7;
            color: #333;
            background: #fafafa;
        }

        h1, h2, h3, h4, h5, h6 { color: #7c3aed; margin-top: 1.8em; }

        h1 { border-bottom: 2px solid #7c3aed; padding-bottom: 10px; }

        code {
            background: rgba(124, 58, 237, 0.08);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "JetBrains Mono", "Courier New", monospace;
            color: #d63384;
            font-size: 0.88em;
        }

        strong { color: #1a1a1a; }
        em { color: #555; }

        ul, ol { padding-left: 1.5em; margin: 1em 0; }
        li { margin: 0.3em 0; }

        blockquote {
            border-left: 4px solid #7c3aed;
            background: #f8f5ff;
            margin: 1em 0;
            padding: 0.5em 1em;
            color: #555;
            border-radius: 0 8px 8px 0;
        }

        blockquote p { margin: 0.3em 0; }

        hr { border: none; border-top: 2px dashed #ccc; margin: 2em 0; }

        /* ============================================================
           Images
           ============================================================ */

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
            margin: 0;
            display: inline-block;
            text-align: center;
        }

        .image-figure figcaption {
            margin-top: 0.5em;
            font-size: 0.85em;
            color: #666;
            font-style: italic;
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
            background: #1e1e2e;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06), 0 8px 24px rgba(0, 0, 0, 0.12);
            transition: box-shadow 0.3s ease;
        }

        .code-block:hover {
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08), 0 12px 32px rgba(124, 58, 237, 0.15);
        }

        .code-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.6em 1em;
            background: #181825;
            border-bottom: 1px solid #313244;
            color: #cdd6f4;
            font-size: 0.8em;
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
            color: #89b4fa;
            opacity: 0.9;
        }

        .code-lang {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-weight: 600;
            color: #89b4fa;
            letter-spacing: 0.02em;
            text-transform: lowercase;
        }

        .code-title {
            font-family: "JetBrains Mono", "Courier New", monospace;
            font-weight: 600;
            color: #cdd6f4;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .code-buttons { display: flex; gap: 0.25em; flex-shrink: 0; }

        .code-btn {
            position: relative;
            display: inline-flex;
            align-items: center;
            gap: 0.35em;
            background: transparent;
            border: 1px solid #45475a;
            border-radius: 6px;
            padding: 0.35em 0.7em;
            cursor: pointer;
            font-size: 0.85em;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-weight: 500;
            color: #cdd6f4;
            transition: background 0.2s cubic-bezier(0.4, 0, 0.2, 1),
                        border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
                        color 0.2s cubic-bezier(0.4, 0, 0.2, 1),
                        transform 0.15s cubic-bezier(0.4, 0, 0.2, 1),
                        box-shadow 0.2s ease;
            overflow: hidden;
            white-space: nowrap;
        }

        .code-btn:hover {
            background: #313244;
            border-color: #89b4fa;
            color: #89b4fa;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .code-btn:active { transform: translateY(0) scale(0.97); }

        .code-btn.success { border-color: #10b981; color: #10b981; }
        .code-btn.active { background: #313244; border-color: #89b4fa; color: #89b4fa; }

        .code-btn svg {
            flex-shrink: 0;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .code-btn:hover svg { transform: scale(1.1); }
        .code-btn.success svg { animation: pop 0.4s cubic-bezier(0.4, 0, 0.2, 1); }

        @keyframes pop {
            0% { transform: scale(1); }
            50% { transform: scale(1.3); }
            100% { transform: scale(1); }
        }

        .code-btn-label { font-size: 0.82em; letter-spacing: 0.01em; }

        .code-body { position: relative; overflow: hidden; }

        .code-block pre {
            margin: 0;
            border-radius: 0;
            background: #1e1e2e;
            padding: 1.1em 1.3em;
            overflow-x: auto;
        }

        .code-block pre code {
            background: transparent;
            color: #cdd6f4;
            padding: 0;
            font-family: "JetBrains Mono", "Fira Code", "Courier New", monospace;
            font-size: 0.86em;
            line-height: 1.65;
            letter-spacing: -0.01em;
        }

        .code-line { display: block; padding: 0 0.5em; margin: 0 -0.5em; }

        .code-line.hl {
            background: rgba(137, 180, 250, 0.1);
            border-left: 3px solid #89b4fa;
            padding-left: calc(0.5em - 3px);
        }

        .line-num {
            display: inline-block;
            width: 2.5em;
            text-align: right;
            color: #6c7086;
            opacity: 0.5;
            margin-right: 1em;
            user-select: none;
        }

        .code-block.wrap pre code {
            white-space: pre-wrap;
            word-break: break-word;
        }

        .code-preview {
            padding: 1.5em;
            background: white;
            border-top: 1px solid #313244;
            color: #222;
            animation: slideDown 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .code-preview * { max-width: 100%; }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 600px) {
            body { margin: 20px auto; padding: 15px; }
            .code-header { padding: 0.5em 0.7em; font-size: 0.75em; }
            .code-btn-label { display: none; }
            .code-btn { padding: 0.35em 0.5em; }
        }
    </style>
</head>
<body>
"""

TAIL = """
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

        var code = getCode(block);
        var lang = (block.dataset.lang || 'html').toLowerCase();

        preview.innerHTML = '';

        if (lang === 'html' || lang === 'markup') {
            var wrapper = document.createElement('div');
            wrapper.style.all = 'initial';
            wrapper.style.display = 'block';
            wrapper.innerHTML = code;
            preview.appendChild(wrapper);
        } else if (lang === 'css') {
            var style = document.createElement('style');
            style.textContent = code;
            preview.appendChild(style);

            var sample = document.createElement('div');
            sample.innerHTML = '<h1>Heading 1</h1><p>This is a sample paragraph to preview your CSS.</p><button>Sample Button</button>';
            preview.appendChild(sample);
        } else if (lang === 'javascript' || lang === 'js') {
            var output = document.createElement('div');
            output.style.fontFamily = 'monospace';
            output.style.fontSize = '14px';
            output.style.background = '#f5f5f5';
            output.style.padding = '12px';
            output.style.borderRadius = '6px';
            output.style.whiteSpace = 'pre-wrap';
            output.style.minHeight = '40px';
            preview.appendChild(output);

            var originalLog = console.log;
            console.log = function() {
                var args = Array.prototype.slice.call(arguments);
                var line = args.map(function(x) {
                    return typeof x === 'object' ? JSON.stringify(x, null, 2) : String(x);
                }).join(' ');
                output.textContent += line + '\\n';
                originalLog.apply(console, arguments);
            };

            try {
                new Function(code)();
            } catch (e) {
                output.textContent += 'Error: ' + e.message;
            }

            setTimeout(function() { console.log = originalLog; }, 100);
        } else {
            preview.textContent = 'Preview not available for this language.';
        }

        preview.removeAttribute('hidden');
        btn.classList.add('active');
    }

    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.code-btn');
        if (!btn) return;

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
    });
})();
</script>
</body>
</html>
"""


def to_html(text: str, title: str = "Markup+ Document") -> str:
    from .parser import parse_text

    doc = parse_text(text)
    body = render_ast(doc)

    head = HEAD.replace("__TITLE__", html.escape(title))
    return head + body + TAIL
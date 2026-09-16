# 🎨 Custom CSS Guide

> **Version:** 0.6.0
> **Audience:** Users who want to customize the appearance of Markup+ documents
> **Prerequisites:** Basic CSS knowledge (helpful but not required)

Learn how to style Markup+ documents with your own CSS files.

---

## 📑 Table of Contents

1. [Quick Start](#1-quick-start)
2. [How It Works](#2-how-it-works)
3. [CSS Variables Reference](#3-css-variables-reference)
4. [Ready-Made Themes](#4-ready-made-themes)
5. [Advanced Customization](#5-advanced-customization)
6. [Complete Example](#6-complete-example)
7. [Tips & Best Practices](#7-tips--best-practices)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Quick Start

### Step 1: Create a CSS file

Create a `.css` file next to your `.mup` file:

```
my-project/
├── document.mup
├── document.html       (generated)
└── my-style.css        ← create this
```

### Step 2: Add CSS variables

Open `my-style.css` and override any variables you want:

```css
:root {
    --accent: #ff6b6b;
    --bg-page: #1a1a2e;
    --text-main: #eaeaea;
}
```

Three lines of CSS. That is all you need.

### Step 3: Convert with the custom CSS

```bash
mup document.mup --css my-style.css
```

### Step 4: Open the result

```bash
start document.html      # Windows
open document.html       # macOS
xdg-open document.html   # Linux
```

Your document now uses the custom theme.

---

## 2. How It Works

Markup+ merges two stylesheets in this order:

1. **`base.css`** — the default stylesheet (always loaded)
2. **Your custom CSS** — appended after `base.css`

Because CSS cascade rules apply, your custom rules **override** the base styles.

### Why this matters

You do **not** need to rewrite the entire stylesheet. Only override the
specific variables or selectors you want to change.

```css
/* ✅ Good — overrides just the accent color */
:root {
    --accent: #ff6b6b;
}
```

```css
/* ❌ Unnecessary — repeating all default styles */
:root {
    --bg-page: #ffffff;
    --bg-soft: #f4f4f5;
    --accent: #ff6b6b;    /* only this line matters */
    --text-main: #18181b;
    /* ... 50 more lines ... */
}
```

---

## 3. CSS Variables Reference

All customizable variables are defined in `:root`. Override any of them in
your custom CSS file.

### Colors

| Variable | Purpose | Default |
|----------|---------|---------|
| `--accent` | Primary color (headings, links, buttons) | `#7c3aed` (purple) |
| `--accent-soft` | Transparent version of accent | `rgba(124, 58, 237, 0.08)` |
| `--accent-hover` | Accent color on hover | `#5b21b6` |
| `--accent-rgb` | RGB values of accent (no `rgb()`) | `124, 58, 237` |
| `--bg-page` | Page background | `#ffffff` |
| `--bg-soft` | Subtle background (TOC, tabs header) | `#f4f4f5` |
| `--bg-code` | Code block background | `#f6f8fa` |
| `--bg-code-header` | Code block header background | `#eaedf0` |
| `--bg-blockquote` | Blockquote background | `#f8f5ff` |
| `--bg-preview` | Code preview background | `#fafafa` |
| `--bg-table-alt` | Alternating table row background | `#f9f9fb` |
| `--bg-table-header` | Table header background | `#f4f4f5` |
| `--text-main` | Primary text color | `#18181b` |
| `--text-soft` | Secondary text color | `#52525b` |
| `--text-muted` | Muted text (captions, footnotes) | `#71717a` |
| `--border` | Default border color | `#e4e4e7` |
| `--border-code` | Code block border | `#d0d7de` |
| `--border-table` | Table border | `#e4e4e7` |
| `--code-text` | Text color inside code blocks | `#24292f` |
| `--code-accent` | Accent inside code blocks (language label) | `#0969da` |

### Typography

| Variable | Purpose | Default |
|----------|---------|---------|
| `--font-body` | Body text font stack | System UI fonts |
| `--font-mono` | Monospace font stack | JetBrains Mono, etc. |
| `--font-size` | Base font size | `16px` |
| `--line-height` | Line height | `1.75` |

### Layout

| Variable | Purpose | Default |
|----------|---------|---------|
| `--max-width` | Maximum content width | `900px` |
| `--padding-x` | Horizontal padding | `24px` |
| `--padding-y` | Vertical padding | `40px` |
| `--radius` | Border radius for large elements | `12px` |
| `--radius-sm` | Border radius for small elements | `8px` |

### Effects

| Variable | Purpose | Default |
|----------|---------|---------|
| `--shadow-sm` | Small shadow | Light |
| `--shadow-md` | Medium shadow | Light |
| `--shadow-lg` | Large shadow | Light |
| `--shadow-xl` | Extra-large shadow (lightbox) | Light |
| `--transition-fast` | Fast transitions | `0.2s` |
| `--transition-med` | Medium transitions | `0.4s` |
| `--transition-slow` | Slow transitions | `0.7s` |

---

## 4. Ready-Made Themes

Copy any of these into a `.css` file and use it with `--css`.

### Ocean Blue

```css
:root {
    --accent: #3b82f6;
    --accent-soft: rgba(59, 130, 246, 0.1);
    --accent-hover: #2563eb;
    --accent-rgb: 59, 130, 246;
    --bg-page: #ffffff;
    --text-main: #0f172a;
    --border: #e2e8f0;
}
```

### Midnight Dark

```css
:root {
    --accent: #a78bfa;
    --accent-soft: rgba(167, 139, 250, 0.15);
    --accent-hover: #c4b5fd;
    --accent-rgb: 167, 139, 250;
    --bg-page: #0f0f1a;
    --bg-soft: #1a1a2e;
    --bg-code: #16162a;
    --bg-code-header: #1f1f3a;
    --bg-blockquote: rgba(167, 139, 250, 0.08);
    --text-main: #e8e8f0;
    --text-soft: #c8c8d8;
    --text-muted: #8888a0;
    --border: #2a2a45;
}
```

### Forest Green

```css
:root {
    --accent: #10b981;
    --accent-soft: rgba(16, 185, 129, 0.1);
    --accent-hover: #059669;
    --accent-rgb: 16, 185, 129;
    --bg-page: #f0fdf4;
    --bg-soft: #dcfce7;
    --text-main: #064e3b;
    --border: #bbf7d0;
}
```

### Rose Pink

```css
:root {
    --accent: #ec4899;
    --accent-soft: rgba(236, 72, 153, 0.1);
    --accent-hover: #db2777;
    --accent-rgb: 236, 72, 153;
    --bg-page: #fdf2f8;
    --bg-soft: #fce7f3;
    --text-main: #831843;
    --border: #fbcfe8;
}
```

### Solarized Light

```css
:root {
    --accent: #268bd2;
    --accent-soft: rgba(38, 139, 210, 0.1);
    --accent-hover: #1e6fa8;
    --bg-page: #fdf6e3;
    --bg-soft: #eee8d5;
    --bg-code: #f5eeda;
    --text-main: #586e75;
    --text-soft: #657b83;
    --text-muted: #93a1a1;
    --border: #eee8d5;
}
```

### Nord

```css
:root {
    --accent: #88c0d0;
    --accent-soft: rgba(136, 192, 208, 0.1);
    --accent-hover: #8fbcbb;
    --bg-page: #2e3440;
    --bg-soft: #3b4252;
    --bg-code: #2e3440;
    --text-main: #eceff4;
    --text-soft: #d8dee9;
    --text-muted: #8fbcbb;
    --border: #434c5e;
}
```

### Paper (High Contrast)

```css
:root {
    --accent: #1a1a1a;
    --accent-soft: rgba(26, 26, 26, 0.08);
    --accent-hover: #000000;
    --bg-page: #faf9f6;
    --bg-soft: #f0eee8;
    --text-main: #1a1a1a;
    --text-soft: #404040;
    --text-muted: #737373;
    --border: #d4d0c8;
    --font-size: 18px;
    --line-height: 1.85;
}
```

---

## 5. Advanced Customization

You can go beyond CSS variables and override any element directly.

### Custom fonts

```css
body {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 18px;
    line-height: 1.8;
}

h1, h2, h3 {
    font-family: "Playfair Display", Georgia, serif;
    font-weight: 700;
}
```

### Gradient headings

```css
h1 {
    background: linear-gradient(135deg, #f472b6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    border-bottom: none;
}
```

### Rounded code blocks with shadows

```css
.code-block {
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.code-block:hover {
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}
```

### Gradient table headers

```css
th {
    background: linear-gradient(135deg, var(--accent), #a78bfa);
    color: white;
    font-weight: 700;
    padding: 14px 18px;
}

.table-wrapper {
    border-radius: 16px;
    overflow: hidden;
}
```

### Styled blockquotes

```css
blockquote {
    border-left: 5px solid var(--accent);
    padding: 20px 28px;
    font-size: 1.1em;
    font-style: italic;
    background: var(--bg-blockquote);
    border-radius: 12px;
    position: relative;
}

blockquote::before {
    content: "\201C";
    position: absolute;
    top: -10px;
    left: 16px;
    font-size: 4em;
    color: var(--accent);
    opacity: 0.3;
    font-family: Georgia, serif;
}
```

### Custom scrollbar

```css
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg-soft);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-hover);
}
```

### Custom selection

```css
::selection {
    background: var(--accent);
    color: white;
}
```

### Custom reading width

```css
body {
    max-width: 1100px;
    padding: 60px 40px 100px;
}
```

### Custom alert boxes

```css
.alert-block {
    border-width: 2px;
    border-radius: 16px;
    padding: 4px;
}

.alert-note {
    background: linear-gradient(135deg,
        rgba(59, 130, 246, 0.1),
        rgba(59, 130, 246, 0.05));
}
```

---

## 6. Complete Example

A full custom theme that demonstrates many features.

Save as `my-beautiful-theme.css`:

```css
/* ============================================================
   My Beautiful Theme
   ============================================================ */

:root {
    /* Colors */
    --accent: #f472b6;
    --accent-soft: rgba(244, 114, 182, 0.12);
    --accent-hover: #ec4899;
    --accent-rgb: 244, 114, 182;

    --bg-page: #0a0a0f;
    --bg-soft: #15151f;
    --bg-code: #1a1a26;
    --bg-code-header: #15151f;
    --bg-blockquote: rgba(244, 114, 182, 0.08);

    --text-main: #f0f0f5;
    --text-soft: #c0c0d0;
    --text-muted: #8080a0;

    --border: #2a2a40;
    --border-code: #2a2a40;

    /* Typography */
    --font-size: 17px;
    --line-height: 1.8;
    --max-width: 960px;
    --padding-x: 32px;
    --padding-y: 56px;
}

/* Gradient headings */
h1 {
    font-size: 2.8em;
    font-weight: 900;
    letter-spacing: -0.03em;
    border: none;
    background: linear-gradient(135deg, #f472b6, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5em;
}

h2 {
    font-size: 1.8em;
    padding-bottom: 12px;
    border-bottom: 2px solid var(--accent-soft);
}

h3 {
    font-size: 1.4em;
    color: var(--accent);
    border-left: 4px solid var(--accent);
    padding-left: 16px;
}

/* Underlined links */
a {
    text-decoration: underline;
    text-underline-offset: 4px;
    text-decoration-thickness: 1px;
    font-weight: 500;
}

a:hover {
    text-decoration-thickness: 2px;
}

/* Floating code blocks */
.code-block {
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(244, 114, 182, 0.1);
    transition: all 0.3s ease;
}

.code-block:hover {
    box-shadow: 0 12px 48px rgba(244, 114, 182, 0.2);
    transform: translateY(-2px);
}

/* Gradient tables */
.table-wrapper {
    border-radius: 16px;
    overflow: hidden;
}

th {
    background: linear-gradient(135deg, var(--accent), #a78bfa);
    color: white;
    font-weight: 700;
    padding: 14px 18px;
}

td {
    padding: 12px 18px;
}

/* Styled blockquotes */
blockquote {
    border-left: 5px solid var(--accent);
    padding: 20px 28px;
    font-size: 1.1em;
    line-height: 1.8;
    background: var(--bg-blockquote);
    border-radius: 12px;
    position: relative;
}

blockquote::before {
    content: "\201C";
    position: absolute;
    top: -10px;
    left: 16px;
    font-size: 4em;
    color: var(--accent);
    opacity: 0.3;
    font-family: Georgia, serif;
}

/* Thicker alert borders */
.alert-block {
    border-width: 2px;
    border-radius: 14px;
    padding: 4px;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 12px;
    height: 12px;
}

::-webkit-scrollbar-track {
    background: var(--bg-soft);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 6px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-hover);
}

/* Custom selection */
::selection {
    background: var(--accent);
    color: white;
}
```

Convert with:

```bash
mup document.mup --css my-beautiful-theme.css
```

---

## 7. Tips & Best Practices

### Use variables first

Always try to solve styling with variables before writing custom selectors.

```css
/* ✅ Preferred */
:root {
    --accent: #ff6b6b;
}
```

```css
/* ❌ Avoid unless necessary */
h1, h2, h3, h4, h5, h6 {
    color: #ff6b6b;
}
a {
    color: #ff6b6b;
}
/* ...and 10 more selectors */
```

### Keep it small

A 20-line CSS file can completely transform the appearance. Start small.

### Test in light and dark mode

If your document will be viewed in both modes, test both:

```bash
mup document.mup --css my-theme.css
mup document.mup --css my-theme.css --dark
```

### Use browser developer tools

Right-click any element in the generated HTML and choose **Inspect**.
The browser will show you exactly which CSS rules apply — useful for
finding the right variable or selector to override.

### Comment your CSS

Future you will thank present you.

```css
:root {
    /* Brand colors — change these to match your project */
    --accent: #ff6b6b;
    --accent-hover: #e94a4a;
}
```

### Version your themes

If you plan to share or reuse a theme, keep it in version control:

```
themes/
├── ocean-blue.css
├── midnight-dark.css
└── forest-green.css
```

### Combine with `--dark`

The `--dark` flag toggles the built-in dark theme, but your custom CSS
still overrides it. This lets you build themes that adapt to both modes:

```css
/* Light mode overrides */
:root {
    --accent: #ff6b6b;
}

/* Dark mode overrides */
[data-theme="dark"] {
    --accent: #ff8888;
}
```

---

## 8. Troubleshooting

### CSS does not apply

**Cause:** File path is wrong, or `--css` flag missing.

**Fix:**

```bash
# Check the file exists
dir my-style.css

# Use absolute path
mup document.mup --css C:\full\path\to\my-style.css
```

### CSS applies but colors do not change

**Cause:** You edited the HTML file directly instead of using `--css`.

**Fix:** Always pass the CSS file to `mup`:

```bash
mup document.mup --css my-style.css     # correct
```

Not:

```bash
mup document.mup                        # then edit HTML manually — wrong
```

### Variable name typo

**Cause:** CSS variables are case-sensitive.

**Wrong:**

```css
:root {
    --Accent: #ff6b6b;    /* capital A — will not work */
    --accentcolor: red;   /* no dash — will not work */
}
```

**Correct:**

```css
:root {
    --accent: #ff6b6b;    /* lowercase with dash — works */
}
```

### Changes not visible

**Cause:** Browser cache.

**Fix:** Hard refresh with `Ctrl+F5` (Windows) or `Cmd+Shift+R` (macOS).

### CSS file not found

**Cause:** Relative path resolved from the wrong directory.

**Fix:** Use an absolute path:

```bash
mup document.mup --css "C:\Users\You\Desktop\my-theme.css"
```

### `--css` flag not recognized

**Cause:** Old version of Markup+ installed.

**Fix:**

```bash
pip install --upgrade markup-plus
mup --version
```

The version should be `0.6.0` or higher.

---

## 📚 Further Reading

- [User Guide](GUIDE.md) — Full syntax reference
- [Developer Guide](DEVELOPER.md) — Architecture and contribution
- [Roadmap](ROADMAP.md) — Future features

### External Resources

- [MDN CSS Reference](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [CSS Variables Guide](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [CSS Cascade](https://developer.mozilla.org/en-US/docs/Web/CSS/Cascade)

---

## 📜 License

MIT License — free to use, modify, and distribute.

Copyright © 2025 Ataee

---

**Last updated:** January 2025
**Version:** 0.6.0
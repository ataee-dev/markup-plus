# 📘 Markup+ — Complete User Guide

> **Version:** 0.6.0
> **Last Updated:** January 2025
> **License:** MIT

A modern markup language that extends Markdown with variables, logic, components,
charts, math, and much more.

---

## 📑 Table of Contents

1. [What is Markup+?](#1-what-is-markup)
2. [Installation](#2-installation)
3. [Quick Start](#3-quick-start)
4. [Basic Syntax](#4-basic-syntax)
5. [Advanced Syntax](#5-advanced-syntax)
6. [Dynamic Logic](#6-dynamic-logic)
7. [Rich Features](#7-rich-features)
8. [CLI Reference](#8-cli-reference)
9. [RTL & Internationalization](#9-rtl--internationalization)
10. [Themes](#10-themes)
11. [FAQ](#11-faq)
12. [Complete Examples](#12-complete-examples)
13. [Tips & Tricks](#13-tips--tricks)
14. [Troubleshooting](#14-troubleshooting)
15. [Coming Soon](#15-coming-soon)

---

## 1. What is Markup+?

**Markup+** is a modern markup language that includes everything Markdown has,
plus powerful features for building documentation, blogs, reports, and
interactive web pages.

### ✨ Why Markup+?

| Feature | Markdown | Markup+ |
|---------|:--------:|:-------:|
| Headings, lists, tables | ✅ | ✅ |
| Bold, italic, links, images | ✅ | ✅ |
| Footnotes | ⚠️ | ✅ |
| Variables | ❌ | ✅ |
| Conditionals (`@if`) | ❌ | ✅ |
| Loops (`@each`) | ❌ | ✅ |
| Reusable components | ❌ | ✅ |
| Charts (bar, line, pie, doughnut) | ❌ | ✅ |
| Math formulas (KaTeX) | ❌ | ✅ |
| Tabs & accordions | ❌ | ✅ |
| Rich alerts (note, warning, tip, danger, success) | ❌ | ✅ |
| Auto RTL detection (Persian, Arabic, Hebrew) | ❌ | ✅ |
| Light & dark themes | ❌ | ✅ |
| Rich code blocks (copy, download, preview) | ❌ | ✅ |
| Image galleries with lightbox | ❌ | ✅ |
| File imports (`@import`) | ❌ | ✅ |

### 🎯 Use Cases

- **Documentation** — API docs, user guides, tutorials
- **Blogs** — technical articles with code and charts
- **Reports** — data-driven reports with charts and tables
- **Academic** — papers with math formulas
- **Persian/Arabic content** — automatic RTL support
- **Static sites** — lightweight alternative to heavy frameworks

---

## 2. Installation

### Requirements

- **Python** 3.9 or higher
- **pip** (comes with Python)

### Install from PyPI

```bash
pip install markup-plus
```

### Verify Installation

```bash
mup --version
```

Expected output:

```
Markup+ v0.6.0
```

### Install from Source (for development)

```bash
git clone https://github.com/USERNAME/markup-plus.git
cd markup-plus
pip install -e .
```

### Uninstall

```bash
pip uninstall markup-plus
```

---

## 3. Quick Start

### Step 1: Create a new file

```bash
mup new my-first-doc
```

This creates `my-first-doc.mup` with starter content.

### Step 2: Write some content

Open `my-first-doc.mup` in any text editor and write:

```mup
# Hello World

This is **bold** text and this is *italic*.

## A List

- First item
- Second item
- Third item

@note
This is a note box.
@end
```

### Step 3: Convert to HTML

```bash
mup my-first-doc.mup
```

Output: `my-first-doc.html`

### Step 4: Open in browser

```bash
start my-first-doc.html    # Windows
open my-first-doc.html     # macOS
xdg-open my-first-doc.html # Linux
```

That's it! You now have a beautiful HTML page.

---

## 4. Basic Syntax

### 4.1 Headings

Use `#` symbols for headings (like Markdown):

```mup
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

**Rules:**
- Must have a space after `#`
- Level 1 has 1 `#`, Level 2 has 2 `#`, up to Level 6
- Headings automatically get anchor IDs for linking

### 4.2 Text Formatting

```mup
**Bold text**
*Italic text*
~~Strikethrough~~
`Inline code`
```

**Combined:**

```mup
**Bold with *italic* inside**
This is **bold** and *italic* together.
```

### 4.3 Lists

**Unordered list:**

```mup
- First item
- Second item
- Third item
```

Also works with `*` or `+`:

```mup
* Item
+ Item
- Item
```

**Ordered list:**

```mup
1. First step
2. Second step
3. Third step
```

**Task list (checklist):**

```mup
- [x] Completed task
- [ ] Pending task
- [x] Another done task
```

Rendered as checkboxes. `[x]` = checked, `[ ]` = unchecked.

### 4.4 Blockquotes

```mup
> This is a quote.
> It can span multiple lines.
>
> And have empty lines too.
```

### 4.5 Horizontal Rules

Three or more dashes, asterisks, or underscores:

```mup
---

***

___
```

### 4.6 Code Blocks

**Inline code:**

```mup
Use `print("Hello")` to print.
```

**Fenced code block:**


```python
def hello(name):
    print(f"Hello, {name}!")

hello("World")
```








# 📘 Markup+ — Complete User Guide

> **Version:** 0.6.0
> **Last Updated:** January 2025
> **License:** MIT

A modern markup language that extends Markdown with variables, logic, components,
charts, math, and much more.

---

## 📑 Table of Contents

1. [What is Markup+?](#1-what-is-markup)
2. [Installation](#2-installation)
3. [Quick Start](#3-quick-start)
4. [Basic Syntax](#4-basic-syntax)
5. [Advanced Syntax](#5-advanced-syntax)
6. [Dynamic Logic](#6-dynamic-logic)
7. [Rich Features](#7-rich-features)
8. [CLI Reference](#8-cli-reference)
9. [RTL & Internationalization](#9-rtl--internationalization)
10. [Themes](#10-themes)
11. [FAQ](#11-faq)
12. [Complete Examples](#12-complete-examples)
13. [Tips & Tricks](#13-tips--tricks)
14. [Troubleshooting](#14-troubleshooting)
15. [Coming Soon](#15-coming-soon)

---

## 1. What is Markup+?

**Markup+** is a modern markup language that includes everything Markdown has,
plus powerful features for building documentation, blogs, reports, and
interactive web pages.

### ✨ Why Markup+?

| Feature | Markdown | Markup+ |
|---------|:--------:|:-------:|
| Headings, lists, tables | ✅ | ✅ |
| Bold, italic, links, images | ✅ | ✅ |
| Footnotes | ⚠️ | ✅ |
| Variables | ❌ | ✅ |
| Conditionals (`@if`) | ❌ | ✅ |
| Loops (`@each`) | ❌ | ✅ |
| Reusable components | ❌ | ✅ |
| Charts (bar, line, pie, doughnut) | ❌ | ✅ |
| Math formulas (KaTeX) | ❌ | ✅ |
| Tabs & accordions | ❌ | ✅ |
| Rich alerts (note, warning, tip, danger, success) | ❌ | ✅ |
| Auto RTL detection (Persian, Arabic, Hebrew) | ❌ | ✅ |
| Light & dark themes | ❌ | ✅ |
| Rich code blocks (copy, download, preview) | ❌ | ✅ |
| Image galleries with lightbox | ❌ | ✅ |
| File imports (`@import`) | ❌ | ✅ |

### 🎯 Use Cases

- **Documentation** — API docs, user guides, tutorials
- **Blogs** — technical articles with code and charts
- **Reports** — data-driven reports with charts and tables
- **Academic** — papers with math formulas
- **Persian/Arabic content** — automatic RTL support
- **Static sites** — lightweight alternative to heavy frameworks

---

## 2. Installation

### Requirements

- **Python** 3.9 or higher
- **pip** (comes with Python)

### Install from PyPI

```bash
pip install markup-plus
```

### Verify Installation

```bash
mup --version
```

Expected output:

```
Markup+ v0.6.0
```

### Install from Source (for development)

```bash
git clone https://github.com/USERNAME/markup-plus.git
cd markup-plus
pip install -e .
```

### Uninstall

```bash
pip uninstall markup-plus
```

---

## 3. Quick Start

### Step 1: Create a new file

```bash
mup new my-first-doc
```

This creates `my-first-doc.mup` with starter content.

### Step 2: Write some content

Open `my-first-doc.mup` in any text editor and write:

```mup
# Hello World

This is **bold** text and this is *italic*.

## A List

- First item
- Second item
- Third item

@note
This is a note box.
@end
```

### Step 3: Convert to HTML

```bash
mup my-first-doc.mup
```

Output: `my-first-doc.html`

### Step 4: Open in browser

```bash
start my-first-doc.html    # Windows
open my-first-doc.html     # macOS
xdg-open my-first-doc.html # Linux
```

That's it! You now have a beautiful HTML page.

---

## 4. Basic Syntax

### 4.1 Headings

Use `#` symbols for headings (like Markdown):

```mup
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6
```

**Rules:**
- Must have a space after `#`
- Level 1 has 1 `#`, Level 2 has 2 `#`, up to Level 6
- Headings automatically get anchor IDs for linking

### 4.2 Text Formatting

```mup
**Bold text**
*Italic text*
~~Strikethrough~~
`Inline code`
```

**Combined:**

```mup
**Bold with *italic* inside**
This is **bold** and *italic* together.
```

### 4.3 Lists

**Unordered list:**

```mup
- First item
- Second item
- Third item
```

Also works with `*` or `+`:

```mup
* Item
+ Item
- Item
```

**Ordered list:**

```mup
1. First step
2. Second step
3. Third step
```

**Task list (checklist):**

```mup
- [x] Completed task
- [ ] Pending task
- [x] Another done task
```

Rendered as checkboxes. `[x]` = checked, `[ ]` = unchecked.

### 4.4 Blockquotes

```mup
> This is a quote.
> It can span multiple lines.
>
> And have empty lines too.
```

### 4.5 Horizontal Rules

Three or more dashes, asterisks, or underscores:

```mup
---

***

___
```

### 4.6 Code Blocks

**Inline code:**

```mup
Use `print("Hello")` to print.
```

**Fenced code block:**

````mup
```python
def hello(name):
    print(f"Hello, {name}!")

hello("World")
```
````

**With title:**

````mup
```python {title="app.py"}
print("Hello")
```
````

**With line numbers:**

````mup
```python {linenos}
print("Hello")
```
````

**With highlight (specific lines):**

````mup
```python {hl=[2,4]}
def add(a, b):
    return a + b

result = add(2, 3)
```
````

**With word wrap:**

````mup
```text {wrap}
Long lines will wrap instead of scrolling horizontally.
```
````

**Disable copy or download:**

````mup
```python {copy=false download=false}
secret_code()
```
````

### 4.7 Links

```mup
[Link text](https://example.com)
[Link with title](https://example.com "Hover text")
<https://auto-link.example.com>
```

Links open in new tab automatically.

### 4.8 Images

**Basic:**

```mup
![Alt text](image.jpg)
```

**With title:**

```mup
![Alt text](image.jpg "Image title")
```

**With width:**

```mup
![Alt](image.jpg){width=400}
```

**With alignment:**

```mup
![Alt](image.jpg){align=center}
![Alt](image.jpg){align=left}
![Alt](image.jpg){align=right}
```

**With caption:**

```mup
![Alt](image.jpg){caption="Figure 1: A beautiful sunset"}
```

**With description (shown in lightbox):**

```mup
![Alt](image.jpg){caption="Figure 1" desc="Longer description shown when zoomed"}
```

**Clickable image:**

```mup
![Alt](image.jpg){link=https://example.com}
```

**Complete example:**

```mup
![Mountain](mountain.jpg){width=600 align=center caption="Mount Everest at sunrise" desc="Photo taken from Kala Patthar at 5,545m" zoomable=true}
```

**Available options:**

| Option | Type | Description |
|--------|------|-------------|
| `width` | number | Width in pixels |
| `height` | number | Height in pixels |
| `align` | `left` / `center` / `right` | Alignment |
| `caption` | string | Shown below image |
| `desc` | string | Shown in lightbox |
| `link` | URL | Wrap image in link |
| `zoomable` | `true` / `false` | Enable lightbox (default: `true`) |

### 4.9 Tables

**Basic table:**

```mup
| Name | Age | City |
|------|-----|------|
| Ali  | 30  | Tehran |
| Sara | 25  | Isfahan |
```

**With alignment:**

```mup
| Left | Center | Right |
|:-----|:------:|------:|
| A    | B      | C     |
```

**Rules:**
- `:---` = left aligned
- `:---:` = center aligned
- `---:` = right aligned
- `---` = default (left)

### 4.10 Footnotes

**Define:**

```mup
This text has a reference[^1].

[^1]: This is the footnote text.
```

**Multiple footnotes:**

```mup
First reference[^a] and second reference[^b].

[^a]: First footnote.
[^b]: Second footnote.
```

Footnotes are collected and displayed at the bottom of the document.

---

## 5. Advanced Syntax

### 5.1 Front Matter

Add metadata at the very top of your file, between `---` lines:

```mup
---
title: My Article
author: Ali Rezaei
date: 2025-01-15
version: 1.0
tags: documentation, tutorial
---

# {title}

By **{author}** — {date}
```

**Available fields** (you can add custom ones):

| Field | Purpose |
|-------|---------|
| `title` | Document title (used in `<title>` tag and can be referenced) |
| `author` | Author name |
| `date` | Publication date |
| `version` | Document version |
| Any custom field | Referenceable via `{fieldname}` |

**Note:** All front matter fields become variables.

### 5.2 Variables (`@let`)

Define reusable values:

```mup
@let name = "Ali"
@let age = 30
@let city = "Tehran"
@let is_active = true
@let pi = 3.14159
@let tags = ["python", "markup", "html"]

Hello **{name}**! You are {age} years old and live in {city}.

Status: {is_active}
Pi: {pi}
First tag: {tags}
```

**Supported types:**

| Type | Example |
|------|---------|
| String | `@let x = "hello"` or `@let x = 'hello'` |
| Integer | `@let x = 42` |
| Float | `@let x = 3.14` |
| Boolean | `@let x = true` / `@let x = false` |
| Null | `@let x = null` |
| Array | `@let x = [1, 2, 3]` |

### 5.3 Filters

Transform variable output with `|`:

```mup
@let name = "markup plus"

{name}                  → markup plus
{name|upper}            → MARKUP PLUS
{name|lower}            → markup plus
{name|capitalize}       → Markup plus
{name|title}            → Markup Plus
{name|reverse}          → sulp pukram
{name|upper|reverse}    → SULP PUKRAM
```

**Available filters:**

| Filter | Effect |
|--------|--------|
| `upper` | Convert to UPPERCASE |
| `lower` | Convert to lowercase |
| `capitalize` | Capitalize first letter |
| `title` | Capitalize Each Word |
| `reverse` | Reverse string (or list) |
| `length` | Return length |

**Filters on arrays:**

```mup
@let items = ["a", "b", "c"]

{items|length}     → 3
{items|reverse}    → ["c", "b", "a"]
```

**Chain filters:**

```mup
{name|upper|reverse}   → Apply upper, then reverse
```

### 5.4 Table of Contents (`@toc`)

**Basic:**

```mup
@toc
```

Generates a TOC from all headings in the document.

**With custom title:**

```mup
@toc {title="Contents"}
@toc {title="On this page"}
@toc {title="فهرست"}       ← Persian works too
```

**Rules:**
- Automatically detects headings from the whole document
- Respects heading hierarchy (H1, H2, H3...)
- Links are clickable and scroll to the section
- Headings in `@if` and `@each` blocks are included

### 5.5 Image Galleries (`@gallery`)

Group images in a responsive grid:

```mup
@gallery {columns=3}
![Sunset](sunset.jpg){caption="Sunset"}
![Mountain](mountain.jpg){caption="Mountain"}
![Ocean](ocean.jpg){caption="Ocean"}
![Forest](forest.jpg){caption="Forest"}
@end
```

**Options:**

```mup
@gallery {columns=2 caption="My Trip Photos"}
![img1](1.jpg)
![img2](2.jpg)
@end
```

| Option | Default | Description |
|--------|---------|-------------|
| `columns` | 3 | Grid columns (1-6) |
| `caption` | (none) | Gallery caption |

**Features:**
- Click any image → opens lightbox
- Keyboard navigation: `←` `→` arrows
- Zoom: mouse scroll or `+` / `-`
- Reset zoom: `0`
- Download: click download button
- `Esc` closes lightbox

### 5.6 File Imports (`@import`)

Split large documents into smaller files:

**`header.mup`:**

```mup
# My Site

Welcome to my site!
```

**`footer.mup`:**

```mup
---

© 2025 My Company
```

**`main.mup`:**

```mup
@import "header.mup"

## Content Section

This is the main content.

@import "footer.mup"
```

**Rules:**
- Paths are relative to the importing file
- Can import files from subdirectories: `@import "parts/intro.mup"`
- Circular imports are detected and prevented
- Missing files show a warning (not an error)
- Imported files can themselves import other files

**Error handling:**

| Problem | Behavior |
|---------|----------|
| File not found | Displays `[Import not found: path]` in output |
| Circular import | Displays `[Circular import: path]` |
| Parse error | Displays `[Import error: path — message]` |

---

## 6. Dynamic Logic

### 6.1 Conditionals (`@if`)

**Basic:**

```mup
@let version = "1.0"

@if version == "1.0"
Stable release!
@endif
```

**With `@else`:**

```mup
@if is_logged_in
Welcome back!
@else
Please log in.
@endif
```

**With `@elif`:**

```mup
@let score = 85

@if score >= 90
Excellent
@elif score >= 70
Good
@elif score >= 50
Average
@else
Needs improvement
@endif
```

**Supported operators:**

| Operator | Meaning |
|----------|---------|
| `==` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |

**Boolean conditions:**

```mup
@if is_active
Active!
@endif

@if not_done
Still pending
@endif
```

### 6.2 Loops (`@each`)

**Basic loop:**

```mup
@let fruits = ["apple", "banana", "cherry"]

@each fruit in fruits
- {fruit}
@end
```

**With index:**

```mup
@let items = ["first", "second", "third"]

@each i, item in items
{i}. {item}
@end
```

**Nested loops:**

```mup
@let matrix = [[1, 2], [3, 4]]

@each row in matrix
@each cell in row
- {cell}
@end
@end
```

**Loop with condition:**

```mup
@let numbers = [1, 2, 3, 4, 5, 6]

@each num in numbers
@if num > 3
- {num} is greater than 3
@endif
@end
```

**Inline array:**

```mup
@each x in [10, 20, 30]
Value: {x}
@end
```

### 6.3 Comments

```mup
@# This is a comment — not rendered

Visible content here.

@# Another comment
```

Comments are skipped during rendering.

---

## 7. Rich Features

### 7.1 Components (`@def`)

Define reusable blocks:

**Definition:**

```mup
@def Card(title, body)
> **{title}**
>
> {body}
@end
```

**Usage:**

```mup
@Card(title="Hello", body="This is a card.")

@Card(title="News", body="Breaking news here!")

@Card(title="Info", body="For more details, see the docs.")
```

**Component with more parameters:**

```mup
@def User(name, email, role)
### {name}

- **Email:** {email}
- **Role:** {role}
@end

@User(name="Ali", email="ali@example.com", role="Admin")

@User(name="Sara", email="sara@example.com", role="Editor")
```

**Rules:**
- Component names must start with UPPERCASE
- Parameters are separated by commas
- Use `{param}` inside the component body
- Components can call other components
- Parameters can use variables from the outer scope

### 7.2 Charts (`@chart`)

**Bar chart:**

```mup
@chart(type="bar" title="Monthly Sales")
data: [100, 250, 180, 320]
labels: ["Jan", "Feb", "Mar", "Apr"]
@end
```

**Line chart:**

```mup
@chart(type="line" title="User Growth")
data: [10, 50, 120, 300, 750]
labels: ["2020", "2021", "2022", "2023", "2024"]
@end
```

**Pie chart:**

```mup
@chart(type="pie" title="Browser Market Share")
data: [55, 20, 15, 10]
labels: ["Chrome", "Firefox", "Safari", "Others"]
@end
```

**Doughnut chart:**

```mup
@chart(type="doughnut" title="OS Distribution")
data: [65, 20, 10, 5]
labels: ["Windows", "macOS", "Linux", "Other"]
@end
```

**Chart types:**

| Type | Best For |
|------|----------|
| `bar` | Comparing categories |
| `line` | Trends over time |
| `pie` | Parts of a whole |
| `doughnut` | Parts of a whole (with hole) |

**Options:**

```mup
@chart(type="bar" title="My Chart" color="#7c3aed")
data: [1, 2, 3]
labels: ["A", "B", "C"]
@end
```

**Notes:**
- `data` values must be numbers
- `labels` values are strings
- Data and labels are matched by position
- Uses Chart.js (loaded from CDN)
- Charts respond to light/dark theme

### 7.3 Math Formulas (KaTeX)

**Block formula (centered):**

```mup
$$ E = mc^2 $$
```

**Inline formula:**

```mup
The famous formula $E = mc^2$ changed physics.
```

**Quadratic formula:**

```mup
$$ x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} $$
```

**Integral:**

```mup
$$ \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2} $$
```

**Matrix:**

```mup
$$ \begin{pmatrix} a & b \\ c & d \end{pmatrix} \cdot \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} ax + by \\ cx + dy \end{pmatrix} $$
```

**Summation:**

```mup
$$ \sum_{i=1}^{n} i = \frac{n(n+1)}{2} $$
```

**Notes:**
- Uses KaTeX syntax
- Rendered client-side (fast)
- Falls back gracefully if syntax error

**Common KaTeX commands:**

| Command | Result |
|---------|--------|
| `\frac{a}{b}` | Fraction |
| `\sqrt{x}` | Square root |
| `\sum_{i=1}^{n}` | Summation |
| `\int_{a}^{b}` | Integral |
| `\alpha`, `\beta`, `\pi` | Greek letters |
| `\pm` | Plus-minus |
| `\cdot` | Dot product |
| `\times` | Times |
| `_n` | Subscript |
| `^n` | Superscript |

### 7.4 Tabs (`@tabs`)

Multiple code samples in tabs:

````mup
@tabs
@tab "Python"
```python
print("Hello from Python")
```
@end

@tab "JavaScript"
```javascript
console.log("Hello from JS");
```
@end

@tab "Bash"
```bash
echo "Hello from Bash"
```
@end
@end
````

**Rules:**
- `@tabs` starts the group
- `@tab "Title"` defines each tab
- Each tab ends with `@end`
- The whole group ends with another `@end`
- First tab is active by default
- Clicking a tab switches panels (JavaScript)

### 7.5 Accordions (`@collapse`)

Collapsible sections (great for FAQs):

````mup
@collapse
@item "What is Markup+?"
Markup+ is a modern markup language.

It extends Markdown with variables, logic, and rich content.
@end

@item "How do I install it?"
Use pip:

```bash
pip install markup-plus
```
@end

@item "Is it free?"
Yes! MIT license.
@end
@end
````

**Rules:**
- `@collapse` starts the group
- `@item "Title"` defines each item
- Each item ends with `@end`
- The whole group ends with another `@end`
- All items start collapsed
- Click header to expand/collapse

### 7.6 Alerts (Callout Boxes)

Five alert types, each with icon and color:

```mup
@note
This is a **note**. Use it for additional information.
@end

@warning
This is a **warning**. Something might go wrong.
@end

@tip
This is a **tip**. A helpful shortcut or suggestion.
@end

@danger
This is **danger**. Critical — could cause damage.
@end

@success
This is **success**. Operation completed successfully.
@end
```

**Visual guide:**

| Type | Icon | Color | Use For |
|------|:----:|:-----:|---------|
| `@note` | ℹ️ | Blue | Additional info |
| `@warning` | ⚠️ | Yellow | Cautions |
| `@tip` | 💡 | Green | Helpful hints |
| `@danger` | 🚨 | Red | Critical warnings |
| `@success` | ✅ | Green | Positive results |

**Alerts can contain anything:**

````mup
@warning
Careful with this command:

```bash
rm -rf /
```

It will delete everything!
@end
````

### 7.7 Rich Quotes (`@quote`)

**With author and source:**

```mup
@quote(author="Hafez", source="Divan")
هر که را جامه ز عشقی چاک شد
او ز عشق مصطفی بی‌باک شد
@end
```

**With author only:**

```mup
@quote(author="Albert Einstein")
Imagination is more important than knowledge.
@end
```

**Using braces instead of parentheses:**

```mup
@quote{author="Douglas Adams", source="Hitchhiker's Guide"}
Don't panic, and always carry a towel.
@end
```

**With variables:**

```mup
@let philosopher = "Socrates"

@quote{author="{philosopher}"}
The unexamined life is not worth living.
@end
```

**Plain quote:**

```mup
@quote
Simple quote without attribution.
@end
```

**Three forms are equivalent:**
- `@quote(author="...", source="...")`
- `@quote{author="...", source="..."}`
- `@quote`

### 7.8 Timeline (`@timeline`)

Display events chronologically:

```mup
@timeline
2020: Project started
2021: First version released
2022: Reached 1,000 users
2023: Major rewrite
2024: Crossed 10,000 users
2025-01-15: v0.6.0 released with rich features
@end
```

**Rules:**
- Each event starts with a date (year, or `YYYY-MM`, or `YYYY-MM-DD`)
- Followed by `:` and the event description
- Rendered as a vertical timeline with dots
- Dates are not parsed — displayed as-is

---

## 8. CLI Reference

### 8.1 Commands

| Command | Description |
|---------|-------------|
| `mup <file>` | Convert `.mup` or `.md` file to HTML |
| `mup new <name>` | Create a new `.mup` file |
| `mup open <file>` | View file in terminal with syntax highlighting |
| `mup check <file>` | Validate file for errors and warnings |
| `mup init [name]` | Initialize a new project |
| `mup serve <file>` | Live server (coming soon) |
| `mup --help` | Show help |
| `mup --version` | Show version |

### 8.2 Options

| Option | Description |
|--------|-------------|
| `-d, --dark` | Use dark theme |
| `-l, --light` | Use light theme (default) |
| `-r, --rtl` | Force right-to-left layout |
| `--ltr` | Force left-to-right layout |
| `-o, --output <file>` | Custom output file path |
| `--debug` | Show debug info (node counts, timing, etc.) |
| `-h, --help` | Show help |
| `-v, --version` | Show version |

### 8.3 Examples

**Basic conversion:**

```bash
mup hello.mup
```

Converts `hello.mup` → `hello.html` (in same folder).

**Markdown conversion:**

```bash
mup readme.md
```

Any `.md` file also works.

**Dark theme:**

```bash
mup report.mup --dark
```

**RTL layout:**

```bash
mup persian.mup --rtl
```

**Custom output path:**

```bash
mup input.mup --output output/custom.html
mup input.mup -o build/index.html
```

**Combined options:**

```bash
mup docs.mup --dark --rtl -o docs/index.html
```

**Create new file:**

```bash
mup new my-doc
```

Creates `my-doc.mup` (adds `.mup` if missing).

**View in terminal:**

```bash
mup open hello.mup
```

Shows the file with syntax highlighting and line numbers.

**Validate:**

```bash
mup check hello.mup
```

Checks for:
- Undefined variables
- Unbalanced blocks (`@if` without `@endif`, etc.)
- Empty documents

**Initialize project:**

```bash
mup init              # In current directory
mup init my-blog      # Create my-blog/ folder
```

Creates:
```
my-blog/
├── docs/
├── assets/
└── index.mup
```

---

## 9. RTL & Internationalization

### 9.1 Auto RTL Detection

Markup+ **automatically** detects right-to-left languages:

- Persian (فارسی)
- Arabic (العربية)
- Hebrew (עברית)
- Urdu (اردو)

If more than 30% of characters are RTL, the entire document becomes RTL.

**Example:**

```mup
# سلام دنیا

این یک متن **فارسی** است.
```

Automatically renders with:
- Right-to-left text direction
- Right-aligned paragraphs
- Persian-friendly fonts
- Reversed list bullets
- Right-side blockquote border

### 9.2 Manual Control

Force a direction:

```bash
mup file.mup --rtl    # Force RTL
mup file.mup --ltr    # Force LTR
```

Useful for:
- Documents with mostly English but Persian title
- Mixed-language documents

### 9.3 Mixed Content

Markup+ handles mixed content gracefully:

- Code blocks stay LTR even in RTL documents
- URLs and emails stay LTR
- Numbers display correctly
- Latin words inline with RTL text

**Example:**

```mup
# راهنمای پایتون

برای نصب از این دستور استفاده کنید:

```bash
pip install markup-plus
```

برای اطلاعات بیشتر به [مستندات](https://example.com) مراجعه کنید.
```

The heading and paragraphs are RTL, but the bash command stays LTR.

---

## 10. Themes

### 10.1 Light Theme (Default)

```bash
mup file.mup
mup file.mup --light
mup file.mup -l
```

- White background
- Dark text
- Purple accents
- Subtle shadows

### 10.2 Dark Theme

```bash
mup file.mup --dark
mup file.mup -d
```

- Dark background (#0a0a0f)
- Light text
- Purple/pink gradient headings
- Enhanced contrast

### 10.3 Switching Themes

Themes are set at conversion time. There's no runtime toggle in the
generated HTML (this may change in future versions).

To offer both, generate two files:

```bash
mup article.mup -o article-light.html
mup article.mup --dark -o article-dark.html
```

### 10.4 Customizing

The generated HTML includes CSS variables. To customize, edit the output
HTML or wrap it in your own stylesheet.

Key CSS variables:

```css
--bg-page:        /* Background */
--text-main:      /* Main text */
--accent:         /* Accent color (purple by default) */
--border:         /* Borders */
--shadow-lg:      /* Large shadows */
```

---

## 11. FAQ

### ❓ What's the difference between Markup+ and Markdown?

Markup+ **is a superset** of Markdown. Everything valid in Markdown is valid
in Markup+, plus:

- Variables and filters
- Conditionals and loops
- Components
- Charts and math
- Tabs and accordions
- Rich code blocks
- Auto RTL detection

### ❓ Can I convert my existing Markdown files?

Yes! Just run:

```bash
mup myfile.md
```

Output is `myfile.html`. Most Markdown features work identically.

### ❓ Is Markup+ a programming language?

Not exactly. It's a **markup language with logic**. You can define variables,
make decisions, and loop — but it's designed for documents, not general
programming.

### ❓ Do I need to know Python?

**No.** You only need Python installed (for the `mup` CLI). You write `.mup`
files in any text editor.

### ❓ Can I use Markup+ offline?

Yes for writing, but the generated HTML uses CDN resources:
- Prism.js (syntax highlighting)
- Chart.js (charts)
- KaTeX (math)

For fully offline use, download these libraries and update the HTML template.

### ❓ What file extension should I use?

Use `.mup` for Markup+ files. `.md` files also work (auto-detected).

### ❓ How do I add a table of contents?

Just add `@toc` where you want it:

```mup
@toc
```

### ❓ How do I create a checklist?

Use task-list syntax:

```mup
- [x] Done
- [ ] Not done
```

### ❓ Can I nest lists?

Indented lists are **not yet supported** in v0.6.0. Flat lists only.

### ❓ Can I use HTML directly?

Some inline HTML passes through. For safety and consistency, prefer Markup+
syntax.

### ❓ How do I create a private link in my document?

Not supported (would require server-side logic).

### ❓ How do I embed a YouTube video?

Use the standard embed:

```mup
![YouTube thumbnail](https://img.youtube.com/vi/VIDEO_ID/0.jpg){link=https://youtube.com/watch?v=VIDEO_ID}
```

Or paste the iframe directly in a code block with `previewable` type.

### ❓ How do I report a bug?

Open an issue on GitHub:
https://github.com/USERNAME/markup-plus/issues

Include:
- The `.mup` file (or minimal reproduction)
- The command you ran
- The error message
- Your Python version (`python --version`)

---

## 12. Complete Examples

### 12.1 Personal Page

```mup
---
title: Ali Rezaei's Page
author: Ali Rezaei
---

# {title}

## About Me

Hi! I'm **{author}**, a software developer from Tehran.

## Skills

- Python
- JavaScript
- Markup+

## Contact

- Email: [ali@example.com](mailto:ali@example.com)
- Website: <https://ali.example.com>
- GitHub: <https://github.com/alirezaei>
```

### 12.2 Project Report

````mup
---
title: Q4 Project Report
date: 2025-01-15
author: Team Alpha
---

# {title}

**Date:** {date}
**Author:** {author}

@toc

## Executive Summary

@note
Project delivered on time. All KPIs exceeded targets.
@end

## Metrics

@chart(type="bar" title="Quarterly Sales")
data: [120, 180, 220, 280]
labels: ["Q1", "Q2", "Q3", "Q4"]
@end

## Team Members

@each name in ["Ali", "Sara", "Reza", "Maryam"]
- **{name}**
@end

## Conclusion

@success
All objectives achieved. Ready for Q1 2026.
@end
````

### 12.3 Tutorial Article

````mup
---
title: Getting Started with Python
author: Ali
date: 2025-01-15
---

# {title}

By **{author}** | {date}

## Installation

@tabs
@tab "Windows"
```bash
python -m pip install --upgrade pip
pip install requests
```
@end

@tab "macOS"
```bash
brew install python
pip install requests
```
@end

@tab "Linux"
```bash
sudo apt install python3 python3-pip
pip install requests
```
@end
@end

## First Script

Create `hello.py`:

```python {title="hello.py"}
import requests

response = requests.get("https://api.github.com")
print(response.status_code)
```

## Common Errors

@warning
If you get `ModuleNotFoundError`, install the module:
```bash
pip install requests
```
@end

@tip
Use a virtual environment to avoid conflicts:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
@end

## Next Steps

- Learn about [async/await](https://docs.python.org/3/library/asyncio.html)
- Explore `requests` documentation
- Build a small project

---

© 2025 {author}
````

### 12.4 Book Chapter

```mup
---
title: Chapter 1 — Introduction
book: Learning Markup+
author: Ali
---

# {title}

*{book}* — by {author}

@toc

## 1.1 Why Markup+?

Markup+ was born from a simple idea: *what if Markdown had superpowers?*

@quote(author="Donald Knuth")
Premature optimization is the root of all evil.
@end

## 1.2 Key Concepts

@each concept in ["Variables", "Components", "Charts", "Math"]
### {concept}

Details about {concept|lower}...
@end

## 1.3 History

@timeline
2020: Project started
2022: First public release
2024: Reached 10,000 users
2025: v0.6.0 with rich features
@end

## 1.4 Summary

@success
You've learned the basics. Move to Chapter 2 for deeper topics.
@end
```

### 12.5 Persian Blog Post

````mup
---
title: راهنمای شروع پایتون
author: علی رضایی
date: ۱۴۰۳/۱۰/۲۵
---

# {title}

نویسنده: **{author}** | تاریخ: {date}

@toc

## معرفی

پایتون یک زبان برنامه‌نویسی **قدرتمند** و *ساده* است.

@note
پایتون در سال ۱۹۹۱ توسط **گیدو ون روسوم** ساخته شد.
@end

## نصب

@tabs
@tab "ویندوز"
```bash
python -m pip install --upgrade pip
```
@end

@tab "لینوکس"
```bash
sudo apt install python3
```
@end
@end

## اولین برنامه

```python {title="hello.py"}
print("سلام دنیا!")
```

## نکات مهم

@tip
همیشه از محیط مجازی استفاده کنید.
@end

@warning
هرگز کد را با دسترسی root اجرا نکنید.
@end

## نتیجه‌گیری

@success
تبریک! شما اولین برنامه پایتون خود را نوشتید.
@end
````

---

## 13. Tips & Tricks

### 💡 Tip 1: Reusable Content

Use components to avoid repetition:

```mup
@def Warning(text)
@warning
{text}
@end
@end

@Warning(text="Don't delete the database!")
@Warning(text="Don't push to main!")
@Warning(text="Don't skip tests!")
```

### 💡 Tip 2: Variables from Front Matter

Front matter becomes variables:

```mup
---
title: My Article
version: 2.0
---

# {title}

Version: **{version}**

For version {version}, install:

```bash
pip install myapp=={version}
```
```

### 💡 Tip 3: Conditional Sections

Show content based on a variable:

```mup
@let environment = "production"

@if environment == "production"
### Production Notes

Deploy with caution.
@else
### Development Notes

Experiment freely.
@endif
```

### 💡 Tip 4: Generate Tables from Data

```mup
@let users = ["Ali", "Sara", "Reza"]

| User | Status |
|------|--------|
@each user in users
| {user} | ✅ |
@end
```

### 💡 Tip 5: Combine Charts with Tables

```mup
@chart(type="bar" title="Sales by Region")
data: [120, 250, 180]
labels: ["North", "South", "East"]
@end

| Region | Sales |
|--------|------:|
| North | 120 |
| South | 250 |
| East | 180 |
```

### 💡 Tip 6: Emoji in Headings

```mup
## 🚀 Quick Start
## 📚 Documentation
## ⚙️ Configuration
```

### 💡 Tip 7: Custom Anchors

Headings automatically get IDs from their text:

```mup
## My Section      → #my-section
## Hello World!    → #hello-world
```

Link to them:

```mup
See [My Section](#my-section) for details.
```

Persian headings also work:

```mup
## سلام دنیا      → #سلام-دنیا
```

### 💡 Tip 8: Split Large Docs with `@import`

**`docs/header.mup`:**

```mup
# My Book

By Ali
```

**`docs/chapter1.mup`:**

```mup
## Chapter 1

Content here.
```

**`docs/book.mup`:**

```mup
@import "header.mup"
@import "chapter1.mup"
```

### 💡 Tip 9: Filter Chains

Combine multiple filters:

```mup
@let title = "hello world"

{title|title}              → Hello World
{title|upper|reverse}      → DLROW OLLEH
{title|capitalize|reverse} → Dlrow olleh
```

### 💡 Tip 10: Debug with `--debug`

See what's happening under the hood:

```bash
mup complex.mup --debug
```

Output includes node counts, timing, variables, and footnotes.

---

## 14. Troubleshooting

### ❌ "mup: command not found"

**Cause:** CLI not installed or PATH not set.

**Fix:**

```bash
python -m pip install --upgrade markup-plus
```

If still failing, use the full module path:

```bash
python -m markup_plus file.mup
```

### ❌ "File is not valid UTF-8"

**Cause:** File contains non-UTF-8 characters.

**Fix:** Save the file as UTF-8 in your editor.

**VS Code:** Bottom-right → click encoding → "Save with Encoding" → UTF-8

**Notepad:** File → Save As → Encoding: UTF-8

### ❌ Variables not replacing

**Cause:** Missing `{` `}` or typo.

**Wrong:**

```mup
@let name = "Ali"

Hello $name!        ← Wrong: use curly braces
Hello (name)!       ← Wrong
Hello {Name}!       ← Wrong: case-sensitive
```

**Correct:**

```mup
Hello {name}!       ← Correct
```

### ❌ Unbalanced blocks

**Cause:** Missing `@end` or `@endif`.

**Fix:** Every block needs to close:

| Opens With | Closes With |
|------------|-------------|
| `@if` | `@endif` (or `@elif` / `@else`) |
| `@each` | `@end` |
| `@def` | `@end` |
| `@tabs` | `@end` |
| `@collapse` | `@end` |
| `@note`/`@warning`/etc. | `@end` |
| `@quote` | `@end` |
| `@chart` | `@end` |
| `@timeline` | `@end` |
| `@gallery` | `@end` |

**Check with:**

```bash
mup check file.mup
```

### ❌ Chart not rendering

**Causes:**
- No internet (Chart.js loads from CDN)
- Invalid data format

**Fix:** Ensure data is an array of numbers:

```mup
@chart(type="bar")
data: [10, 20, 30]        ← Correct
labels: ["A", "B", "C"]
@end
```

**Wrong:**

```mup
data: [10, "twenty", 30]  ← Wrong: mixed types
data: 10, 20, 30          ← Wrong: missing brackets
```

### ❌ Math not rendering

**Cause:** Syntax error in LaTeX.

**Fix:** Check KaTeX syntax. Test at https://katex.org/

### ❌ RTL layout not activating

**Cause:** Less than 30% RTL characters.

**Fix:** Force it:

```bash
mup file.mup --rtl
```

### ❌ Import not working

**Causes:**
- Wrong path
- Circular import
- File doesn't exist

**Fix:** Check with absolute paths and look for `[Import not found: ...]`
in the output HTML.

### ❌ Output HTML is huge

**Cause:** Large document or many charts.

**Fix:** Split with `@import`. Reduce chart data. This is expected behavior.

---

## 15. Coming Soon

Features planned for future versions:

### v0.7.0
- ⏳ `@run` — Execute HTML/JS code in-place
- ⏳ Nested lists
- ⏳ Tables with cell spanning
- ⏳ HTML export options (standalone, fragments)

### v0.8.0
- ⏳ Live preview server (`mup serve`)
- ⏳ PDF export
- ⏳ Custom templates
- ⏳ Plugin system

### v1.0.0
- ⏳ Stable API
- ⏳ Full documentation site
- ⏳ Desktop IDE
- ⏳ Windows installer

### Long-term
- ⏳ VS Code extension
- ⏳ Online editor
- ⏳ Cloud sync
- ⏳ Collaborative editing

---

## 📚 Additional Resources

- **GitHub Repository:** https://github.com/USERNAME/markup-plus
- **Issue Tracker:** https://github.com/USERNAME/markup-plus/issues
- **Discussions:** https://github.com/USERNAME/markup-plus/discussions
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Developer Guide:** [DEVELOPER.md](DEVELOPER.md)
- **Tutorial:** [TUTORIAL.md](TUTORIAL.md)

---

## 📜 License

MIT License — free to use, modify, and distribute.

Copyright © 2025 Ataee

---

**Made with 💜 using Markup+ v0.6.0**
````

---

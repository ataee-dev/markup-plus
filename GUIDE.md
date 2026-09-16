
---

## 🤔 What is Markup+?

Imagine taking **Markdown** (the language you use on GitHub, Discord, etc.) and giving it **superpowers**. You keep the same simplicity, but now you can:

- Create **variables** (e.g., `name = "John"` and later write `{name}` to output John)
- Use **conditionals** (if something is true, show this)
- Write **loops** (repeat something for each item in a list)
- Build **components** (a reusable template you use multiple times)
- Draw **charts** (bar, line, pie, doughnut)
- Write **math formulas**
- Create **tabs** and **accordions**
- And much more...

At the end, it all converts into an **HTML file** you can open in any browser.

---

## 📦 Installation

```bash
pip install markup-plus
```

Then verify:

```bash
mup --version
```

Expected output: `Markup+ v0.6.0`

> 💡 **Note:** You only need Python installed. You don't need to know Python — it just has to be on your system.

---

## 🚀 Quick Start

**Step 1:** Create a new file:

```bash
mup new my-first-doc
```

This creates a file called `my-first-doc.mup`.

**Step 2:** Write this inside:

```mup
# Hello World

This is **bold** and this is *italic*.

@note
This is a note box.
@end
```

**Step 3:** Convert it to HTML:

```bash
mup my-first-doc.mup
```

**Step 4:** Open `my-first-doc.html` in your browser. Done! 🎉

---

## 🧩 Core Concepts (in order)

Let me walk through the important parts, one by one.

### 1️⃣ Front Matter (metadata at the top)

At the top of the file, between `---`, you can write metadata:

```mup
---
title: My Article
author: John Doe
date: 2025-01-15
---

# {title}

By **{author}**
```

Here, `title` and `author` become **variables**. Anywhere you write `{title}`, the value appears.

### 2️⃣ Variables (`@let`)

```mup
@let name = "John"
@let age = 30

Hello **{name}**! You are {age} years old.
```

Output: Hello **John**! You are 30 years old.

### 3️⃣ Filters (`|`)

You can transform text:

```mup
@let name = "markup plus"

{name|upper}       → MARKUP PLUS
{name|title}       → Markup Plus
{name|reverse}     → sulp pukram
```

### 4️⃣ Conditionals (`@if`)

```mup
@let score = 85

@if score >= 90
Excellent
@elif score >= 70
Good
@else
Needs improvement
@endif
```

Output: **Good** (since 85 is between 70 and 90)

### 5️⃣ Loops (`@each`)

```mup
@let fruits = ["apple", "banana", "cherry"]

@each fruit in fruits
- {fruit}
@end
```

Output:
- apple
- banana
- cherry

### 6️⃣ Components (`@def`)

A reusable template:

```mup
@def Card(title, body)
> **{title}**
>
> {body}
@end

@Card(title="News", body="Something important!")
@Card(title="Info", body="More details...")
```

### 7️⃣ Charts (`@chart`)

```mup
@chart(type="bar" title="Monthly Sales")
data: [100, 250, 180, 320]
labels: ["Jan", "Feb", "Mar", "Apr"]
@end
```

Chart types: `bar`, `line`, `pie`, `doughnut`

### 8️⃣ Math Formulas

```mup
$$ E = mc^2 $$

The famous formula $E = mc^2$ changed physics.
```

### 9️⃣ Tabs (`@tabs`)

```mup
@tabs
@tab "Python"
```python
print("Hello")
```
@end

@tab "JavaScript"
```javascript
console.log("Hello");
```
@end
@end
```

### 🔟 Accordions (`@collapse`) — great for FAQs

```mup
@collapse
@item "What is Markup+?"
A modern markup language.
@end

@item "How do I install it?"
Install it with pip.
@end
@end
```

### 1️⃣1️⃣ Alerts (colored boxes)

```mup
@note
A regular note (blue)
@end

@warning
A warning (yellow)
@end

@tip
A helpful tip (green)
@end

@danger
Danger (red)
@end

@success
Success (green)
@end
```

### 1️⃣2️⃣ Quotes (`@quote`)

```mup
@quote(author="Albert Einstein", source="Unknown")
Imagination is more important than knowledge.
@end
```

### 1️⃣3️⃣ Timeline (`@timeline`)

```mup
@timeline
2020: Project started
2022: First release
2024: 10,000 users
2025: v0.6.0 released
@end
```

### 1️⃣4️⃣ Image Galleries (`@gallery`)

```mup
@gallery {columns=3}
![Sunset](sunset.jpg){caption="Sunset"}
![Mountain](mountain.jpg){caption="Mountain"}
@end
```

### 1️⃣5️⃣ Imports (`@import`)

Split large documents into smaller files:

```mup
@import "header.mup"
@import "chapter1.mup"
```

---

## 💻 CLI Commands

| Command | What it does |
|---------|-------------|
| `mup file.mup` | Convert to HTML |
| `mup new name` | Create a new file |
| `mup check file.mup` | Validate for errors |
| `mup open file.mup` | View in terminal |
| `mup init` | Initialize a new project |
| `mup --dark` | Dark theme |
| `mup --rtl` | Right-to-left layout |
| `mup -o out.html` | Custom output path |

**Combined example:**

```bash
mup docs.mup --dark --rtl -o docs/index.html
```

---

## 🌍 RTL (Right-to-Left) Support

Markup+ **automatically** detects right-to-left languages (Persian, Arabic, Hebrew, Urdu). If more than 30% of characters are RTL, the entire document becomes RTL.

To force it manually:

```bash
mup file.mup --rtl    # Force RTL
mup file.mup --ltr    # Force LTR
```

---

## ❓ FAQ

**Q: How is Markup+ different from Markdown?**
A: Markup+ is a **superset** of Markdown. Everything that works in Markdown works here, plus many extra features.

**Q: Can I convert my old `.md` files?**
A: Yes! Just run `mup myfile.md` — it auto-detects.

**Q: Do I need to know Python?**
A: No! You only need Python installed. You write `.mup` files in any text editor.

**Q: Does it work offline?**
A: Writing works offline, but the generated HTML uses CDN resources for charts and math. For fully offline use, download the libraries locally.

**Q: Are nested lists supported?**
A: Not yet in v0.6.0. Only flat lists. Coming in a future version.

---

## 🛠️ Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| `mup: command not found` | `python -m pip install --upgrade markup-plus` |
| File is not UTF-8 | Save as UTF-8 in your editor |
| Variables not replacing | Check that `{name}` is correct (case-sensitive) |
| Unbalanced blocks | Run `mup check file.mup` |
| Chart not rendering | No internet (CDN) or invalid data format |
| RTL not activating | Force it with `--rtl` |

---

## 🔮 Coming Soon

- **v0.7.0:** Run HTML/JS code in-place, nested lists, tables with cell spanning
- **v0.8.0:** Live preview server, PDF export, custom templates
- **v1.0.0:** Stable API, full documentation site, desktop app

---

## 🎓 One-Line Summary

> **Markdown + variables + conditionals + loops + components + charts + math + auto RTL = Markup+**

Everything you know from Markdown still works — you just get more powerful features on top.

---

---

## 📚 Full Reference

For the complete syntax reference (all directives, all options, all examples),
see **[GUIDE-FOR-AI.md](GUIDE-FOR-AI.md)**.

---

## 🎓 One-Line Summary

> **Markdown + variables + conditionals + loops + components + charts + math + auto RTL = Markup+**

Everything you know from Markdown still works — you just get more powerful features on top.
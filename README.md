<div align="center">

<img src="assets/images/mup-logo.png" alt="Markup+ Logo" width="150">

# Markup+

**A modern markup language with more features than Markdown.**

[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](https://github.com/ataee-dev/markup-plus/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Non--Commercial-red.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-174%20passing-success.svg)](tests/)

[Installation](#installation) • [Quick Start](#quick-start) • [Features](#features) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## What is Markup+

Markup+ is a modern markup language that extends Markdown with powerful features for building documentation, blogs, reports, and interactive web pages.

Everything you know from Markdown still works — you just get more powerful features on top:

- **Variables and filters** — reusable values with transformations
- **Conditionals and loops** — dynamic content generation
- **Reusable components** — define once, use many times
- **Charts** — bar, line, pie, doughnut
- **Math formulas** — via KaTeX
- **Tabs and accordions** — organized content
- **Rich alerts** — 5 types of callout boxes
- **Auto RTL detection** — for Persian, Arabic, Hebrew, Urdu
- **Image galleries** — with lightbox
- **File imports** — split large documents

---

## Features

| Feature | Markdown | Markup+ |
|---------|:--------:|:-------:|
| Headings, lists, tables | ✅ | ✅ |
| Bold, italic, links, images | ✅ | ✅ |
| Footnotes | Partial | ✅ |
| Variables | ❌ | ✅ |
| Conditionals (`@if`) | ❌ | ✅ |
| Loops (`@each`) | ❌ | ✅ |
| Reusable components | ❌ | ✅ |
| Charts | ❌ | ✅ |
| Math formulas | ❌ | ✅ |
| Tabs and accordions | ❌ | ✅ |
| Rich alerts | ❌ | ✅ |
| Auto RTL detection | ❌ | ✅ |
| Light and dark themes | ❌ | ✅ |
| Custom CSS | ❌ | ✅ |
| Image galleries | ❌ | ✅ |
| File imports | ❌ | ✅ |

---

## Installation

### Windows (Standalone Installer)

Download the installer from the [latest release](https://github.com/ataee-dev/markup-plus/releases/latest) and run it. No Python required.

### pip install (For Developers)

Requires Python 3.9 or higher.

```bash
pip install markup-plus
```

Verify:

```bash
mup --version
```

Expected output: `Markup+ v0.6.0`

---

## Quick Start

### Step 1: Create a new file

```bash
mup new my-first-doc
```

### Step 2: Write content

```markup
# Hello World

This is **bold** and this is *italic*.

@note
This is a note box.
@end
```

### Step 3: Convert to HTML

```bash
mup my-first-doc.mup
```

### Step 4: Open in browser

```bash
start my-first-doc.html    # Windows
open my-first-doc.html     # macOS
xdg-open my-first-doc.html # Linux
```

---

## Core Concepts

1. **Front Matter** — metadata at the top of the file
2. **Variables** (`@let`) — reusable values
3. **Filters** (`|`) — transform text
4. **Conditionals** (`@if`) — show or hide content
5. **Loops** (`@each`) — repeat content
6. **Components** (`@def`) — reusable templates
7. **Charts** (`@chart`) — bar, line, pie, doughnut
8. **Math** — KaTeX formulas
9. **Tabs** (`@tabs`) — multiple code samples
10. **Accordions** (`@collapse`) — collapsible sections

---

## CLI Commands

```bash
mup file.mup              Convert to HTML
mup new name              Create a new file
mup check file.mup        Validate for errors
mup open file.mup         View in terminal
mup init                  Initialize a new project
mup file.mup --dark       Dark theme
mup file.mup --rtl        Right-to-left layout
mup file.mup --css x.css  Custom CSS
mup file.mup -o out.html  Custom output path
mup file.mup --debug      Show debug info
```

---

## Documentation

- [User Guide](docs/GUIDE.md) — Complete reference
- [Installation](docs/INSTALL.md) — Detailed setup
- [Tutorial](docs/TUTORIAL.md) — Step-by-step learning
- [Developer Guide](docs/DEVELOPER.md) — Architecture and contribution
- [Custom CSS](docs/CUSTOM-CSS.md) — Theming and customization
- [FAQ](docs/FAQ.md) — Frequently asked questions
- [Changelog](CHANGELOG.md) — Version history
- [Roadmap](ROADMAP.md) — Future plans

---

## Project Statistics

- Total features: 45
- Total tests: 174
- Total phases completed: 5
- Total versions released: 6

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Security

See [SECURITY.md](SECURITY.md) for our security policy.

---

## License

**Markup+ Non-Commercial License**

Copyright © 2026 Hossein Ataee

See [LICENSE](LICENSE) for full text.

---

## Contact

- **Email:** hosseinataee2009@gmail.com
- **Repository:** https://github.com/ataee-dev/markup-plus
- **Issues:** https://github.com/ataee-dev/markup-plus/issues
- **Discussions:** https://github.com/ataee-dev/markup-plus/discussions
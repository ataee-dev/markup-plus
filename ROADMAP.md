Roadmap
=======

Version: 0.6.0
Last Updated: September 2026

This document outlines the development history of Markup+.

For the full version history, see CHANGELOG.md.
For current work, see GitHub Issues:
https://github.com/ataee-dev/markup-plus/issues

---

Vision
------

Markup+ aims to be:

1. The most feature-rich markup language -- everything Markdown has,
   plus powerful logic
2. Beginner-friendly -- no programming knowledge required
3. Beautiful by default -- professional output with zero configuration
4. RTL-first for Persian and Arabic -- built-in bidirectional text support
5. Extensible -- plugin system, custom renderers, IDE integration

---

Version History
---------------

### v0.1.0 -- Phase 1: Core

Released: September 15, 2026

- Headings (H1 to H6)
- Paragraphs
- Bold and italic formatting
- Inline code
- Basic HTML output
- CLI entry point
- Blockquotes and horizontal rules (Phase 2.2)
- Enhanced code blocks with live preview (Phase 2.3.5)

### v0.2.0 -- Phase 2.4: Images

Released: September 15, 2026

- Image syntax with `![alt](url)`
- Image options: width, height, align, caption, description, link, zoomable
- Image alignment (left, center, right)
- Image captions
- Clickable images

### v0.3.0 -- Phase 2.5: Complete feature set

Released: September 15, 2026

- Image lightbox with keyboard navigation
- Light and dark themes
- Scroll reveal animations
- Theme switcher

### v0.3.1 -- Phase 3.1: Links and formatting

Released: September 15, 2026

- Link syntax with `[text](url)` and `[text](url "title")`
- Autolinks with `<https://example.com>`
- Strikethrough with `~~text~~`
- Links open in new tab

### v0.3.2 -- Phase 3.2: Tables

Released: September 15, 2026

- Markdown-style tables
- Column alignment: left, center, right
- Table header styling
- Alternating row colors

### v0.3.3 -- Phase 3.3: Auto RTL

Released: September 16, 2026

- Automatic RTL detection for Persian, Arabic, Hebrew, Urdu
- 30 percent RTL character threshold
- `--rtl` and `--ltr` flags
- Persian-friendly fonts and layout

### v0.4.0 -- Phase 3.4-3.5: Task lists and TOC

Released: September 16, 2026

- Task lists with checkboxes (`- [x]` and `- [ ]`)
- Front matter support for metadata
- Table of contents directive (`@toc`)
- Footnotes support with `[^1]` syntax

### v0.5.0 -- Phase 4: Variables and Logic

Released: September 16, 2026

- Variable system (`@let`) with strings, numbers, booleans, arrays
- Conditional blocks (`@if`, `@elif`, `@else`, `@endif`)
- Loop blocks (`@each` with optional index)
- Filter system: `upper`, `lower`, `capitalize`, `title`, `reverse`, `length`
- Comment directive (`@#`)
- Variable substitution with `{name}`
- Filter chaining with `|`

### v0.6.0 -- Phase 5: Rich Features

Released: September 16, 2026

- Alert directives: `@note`, `@warning`, `@tip`, `@danger`, `@success`
- Rich quote directive (`@quote`) with author and source
- Tabs directive (`@tabs` and `@tab`)
- Accordion directive (`@collapse` and `@item`)
- Chart directive (`@chart`) with bar, line, pie, doughnut
- Math formulas with KaTeX (inline and block)
- Component system (`@def` and component calls)
- Timeline directive (`@timeline`)
- File imports (`@import`)
- Table of contents directive (`@toc`) with custom title
- Custom CSS support via `--css` flag
- Ready-made themes
- Standalone executable for Windows

---

Project Statistics
------------------

Statistics as of v0.6.0:

    Phase      Feature                          Tests
    Phase 1    Core                               11
    Phase 2    Blocks and Images                 ~50
    Phase 2.5  Rich Code and Lightbox            ~95
    Phase 3    Tables, TOC, Footnotes             126
    Phase 4    Variables, Logic, Loops            174
    Phase 5    Components, Charts, Math          ~220

Total features: 45
Total tests: ~220
Total phases completed: 5
Total versions released: 6

---

Feature Requests
----------------

Want a feature not on this list? Open an issue:

https://github.com/ataee-dev/markup-plus/issues/new

---

Out of Scope
------------

These are not planned for Markup+:

- General-purpose programming -- use Python or JavaScript
- Server-side logic -- use a web framework
- Database ORM -- use SQLAlchemy
- Full CMS -- use WordPress or Strapi
- Real-time apps -- use React or Vue
- Mobile apps -- use React Native or Flutter

Markup+ stays focused on static document generation and content markup.

---

Discuss the Roadmap
-------------------

Have thoughts? Join the discussion:

- GitHub Discussions: https://github.com/ataee-dev/markup-plus/discussions
- Feature Requests: https://github.com/ataee-dev/markup-plus/issues/new
- Email: hosseinataee2009@gmail.com

---

Contact
-------

- Email: hosseinataee2009@gmail.com
- Repository: https://github.com/ataee-dev/markup-plus
- Issues: https://github.com/ataee-dev/markup-plus/issues
- Discussions: https://github.com/ataee-dev/markup-plus/discussions

---

Last updated: September 2026

Markup+ Non-Commercial License
Copyright 2026 Hossein Ataee
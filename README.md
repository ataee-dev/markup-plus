Markup+
=======

Version: 0.6.0
Last Updated: January 2026
License: Markup+ Non-Commercial License
Copyright 2026 Hossein Ataee
Email: hosseinataee2009@gmail.com
Repository: https://github.com/ataee-dev/markup-plus

---

A modern markup language with more features than Markdown.

Markup+ extends Markdown with variables, logic, components, charts,
math, and much more. Everything you know from Markdown still works --
you just get more powerful features on top.

---

## Why Markup+

| Feature | Markdown | Markup+ |
|---------|:--------:|:-------:|
| Headings, lists, tables | Yes | Yes |
| Bold, italic, links, images | Yes | Yes |
| Footnotes | Partial | Yes |
| Variables | No | Yes |
| Conditionals (`@if`) | No | Yes |
| Loops (`@each`) | No | Yes |
| Reusable components | No | Yes |
| Charts | No | Yes |
| Math formulas | No | Yes |
| Tabs and accordions | No | Yes |
| Rich alerts | No | Yes |
| Auto RTL detection | No | Yes |
| Light and dark themes | No | Yes |
| File imports | No | Yes |

---

## Installation

    pip install markup-plus

Verify:

    mup --version

Expected output:

    Markup+ v0.6.0

---

## Quick Start

Step 1: Create a new file.

    mup new my-first-doc

Step 2: Write content.

    # Hello World

    This is **bold** and this is *italic*.

    @note
    This is a note box.
    @end

Step 3: Convert to HTML.

    mup my-first-doc.mup

Step 4: Open my-first-doc.html in your browser.

---

## Core Concepts

1. Front Matter -- metadata at the top of the file
2. Variables (`@let`) -- reusable values
3. Filters (`|`) -- transform text
4. Conditionals (`@if`) -- show or hide content
5. Loops (`@each`) -- repeat content
6. Components (`@def`) -- reusable templates
7. Charts (`@chart`) -- bar, line, pie, doughnut
8. Math -- KaTeX formulas
9. Tabs (`@tabs`) -- multiple code samples
10. Accordions (`@collapse`) -- collapsible sections

---

## CLI Commands

    mup file.mup              Convert to HTML
    mup new name              Create a new file
    mup check file.mup        Validate for errors
    mup open file.mup         View in terminal
    mup init                  Initialize a new project
    mup --dark                Dark theme
    mup --rtl                 Right-to-left layout
    mup -o out.html           Custom output path

---

## Documentation

- [User Guide](docs/GUIDE.md)
- [Tutorial](docs/TUTORIAL.md)
- [Developer Guide](docs/DEVELOPER.md)
- [Custom CSS](docs/CUSTOM-CSS.md)
- [FAQ](docs/FAQ.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines.

---

## Security

See [SECURITY.md](SECURITY.md) for our security policy.

---

## License

Markup+ Non-Commercial License.

Copyright 2026 Hossein Ataee.

See [LICENSE](LICENSE) for full text.

---

## Contact

- Email: hosseinataee2009@gmail.com
- Repository: https://github.com/ataee-dev/markup-plus
- Issues: https://github.com/ataee-dev/markup-plus/issues
- Discussions: https://github.com/ataee-dev/markup-plus/discussions
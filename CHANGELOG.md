Changelog
=========

All notable changes to Markup+ will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- `@run` directive for executing HTML/JS/CSS in-place
- Nested lists support
- Table cell spanning
- PDF export
- Live preview server
- Plugin system

---

## [0.6.1] - 2026-09-17

### Fixed
- Logo now displays correctly on PyPI (uses absolute URL)

### Changed
- Updated README with absolute logo URL for PyPI compatibility

---


## [0.6.0] - 2026-09-16

Release v0.6.0: Custom CSS, themes, standalone exe.

### Added
- Custom CSS support via `--css` flag
- Ready-made themes (Ocean Blue, Midnight Dark, Forest Green, Rose Pink, Solarized Light, Nord, Paper)
- Standalone executable for Windows
- Theme switching at conversion time
- Complete CSS variables system for customization

### Changed
- Improved rendering pipeline
- Enhanced theme system

### Fixed
- Various rendering issues from previous versions

---

## [0.5.0] - 2026-09-16

Phase 4: Variables, if/elif/else, each loops, filters, and comments.

### Added
- Variable system (`@let`) with strings, numbers, booleans, and arrays
- Conditional blocks (`@if`, `@elif`, `@else`, `@endif`)
- Loop blocks (`@each` with optional index)
- Filter system with `upper`, `lower`, `capitalize`, `title`, `reverse`, `length`
- Comment directive (`@#`)
- Variable substitution with `{name}` syntax
- Filter chaining with `|`

### Changed
- Parser now tracks variable definitions
- Renderer evaluates conditions and loops

---

## [0.4.0] - 2026-09-16

Phase 3.4-3.5: Task lists, front matter, TOC, and footnotes.

### Added
- Task lists with checkboxes (`- [x]` and `- [ ]`)
- Front matter support for metadata (between `---` lines)
- Table of contents directive (`@toc`) with custom title
- Footnotes support with `[^1]` syntax
- Front matter fields become variables

### Changed
- Parser handles front matter as metadata
- TOC automatically generated from headings

---

## [0.3.3] - 2026-09-16

Phase 3.3: Auto RTL detection for Persian, Arabic, Hebrew.

### Added
- Automatic RTL detection for Persian, Arabic, Hebrew, and Urdu
- 30% RTL character threshold for auto-detection
- `--rtl` and `--ltr` flags for manual control
- Persian-friendly fonts and layout

### Changed
- Direction detection algorithm uses Unicode bidirectional properties

### Fixed
- RTL rendering for mixed Persian and English text

---

## [0.3.2] - 2026-09-15

Phase 3.2: Tables with alignment support.

### Added
- Markdown-style tables with `|` syntax
- Column alignment: left (`:---`), center (`:---:`), right (`---:`)
- Table header styling
- Alternating row colors

### Fixed
- Table rendering with special characters

---

## [0.3.1] - 2026-09-15

Phase 3.1: Links, autolinks, strikethrough + test updates.

### Added
- Link syntax with `[text](url)` and `[text](url "title")`
- Autolinks with `<https://example.com>`
- Strikethrough with `~~text~~`
- Links open in new tab automatically

### Changed
- Test suite updates for new features

---

## [0.3.0] - 2026-09-15

Phase 2.5: Complete feature set - lightbox, themes, scroll reveal.

### Added
- Image lightbox with keyboard navigation
- Light and dark themes
- Scroll reveal animations
- Theme switcher

### Changed
- Complete redesign of image rendering
- Enhanced visual presentation

---

## [0.2.0] - 2026-09-15

Phase 2.4: Images with alignment, captions, links, and options.

### Added
- Image syntax with `![alt](url)`
- Image options: width, height, align, caption, description, link, zoomable
- Image alignment (left, center, right)
- Image captions below images
- Clickable images with links

### Changed
- Image rendering with wrapper elements

---

## [0.1.0] - 2026-09-15

Phase 1: Core - headings, paragraphs, inline formatting.

### Added
- Heading support (H1 to H6)
- Paragraph support
- Bold (`**text**`) and italic (`*text*`) formatting
- Inline code with backticks
- Basic HTML output
- CLI entry point (`mup` command)

### Added (within v0.1.0 development)
- Phase 2.2: Blockquotes and horizontal rules
- Phase 2.3.5: Enhanced code blocks with live preview
- Fenced code blocks with syntax highlighting
- Code block copy and download buttons
- Live preview for HTML/CSS/JS code

---

## Version History Summary

| Version | Date | Phase | Focus |
|---------|------|-------|-------|
| 0.1.0 | 2026-09-15 | Phase 1-2.3 | Core + Blockquotes + Code blocks |
| 0.2.0 | 2026-09-15 | Phase 2.4 | Images with options |
| 0.3.0 | 2026-09-15 | Phase 2.5 | Lightbox + Themes + Scroll reveal |
| 0.3.1 | 2026-09-15 | Phase 3.1 | Links + Autolinks + Strikethrough |
| 0.3.2 | 2026-09-15 | Phase 3.2 | Tables with alignment |
| 0.3.3 | 2026-09-16 | Phase 3.3 | Auto RTL detection |
| 0.4.0 | 2026-09-16 | Phase 3.4-3.5 | Task lists + Front matter + TOC + Footnotes |
| 0.5.0 | 2026-09-16 | Phase 4 | Variables + Conditionals + Loops + Filters |
| 0.6.0 | 2026-09-16 | Release | Custom CSS + Themes + Standalone exe |

---

## Upcoming Versions

### [0.7.0] - Planned
- `@run` directive for executing HTML/JS/CSS in-place
- Nested lists
- Table cell spanning
- Better error messages with line context
- Auto-fix suggestions
- Watch mode (`mup watch`)

### [0.8.0] - Planned
- PDF export
- Markdown export
- EPUB export
- JSON export
- Static site generation
- Custom HTML templates

### [0.9.0] - Planned
- Incremental compilation
- Streaming parser
- Parallel rendering
- Plugin system
- Built-in plugins

### [1.0.0] - Planned
- Stable API
- 100% test coverage on core modules
- Desktop IDE (Markup+ Studio)
- Windows installer
- Documentation website
- Video course

---

## Links

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [Markup+ Repository](https://github.com/ataee-dev/markup-plus)
- [Markup+ Issues](https://github.com/ataee-dev/markup-plus/issues)
- [Markup+ Discussions](https://github.com/ataee-dev/markup-plus/discussions)

---

## Contact

- Email: hosseinataee2009@gmail.com
- Repository: https://github.com/ataee-dev/markup-plus

---

Markup+ Non-Commercial License
Copyright 2026 Hossein Ataee
# 🗺️ Markup+ Roadmap

This document outlines the **planned development** of Markup+.

For the past, see [CHANGELOG.md](CHANGELOG.md).
For current work, see [GitHub Issues](https://github.com/USERNAME/markup-plus/issues).

---

## 🎯 Vision

Markup+ aims to be:

1. **The most feature-rich markup language** — everything Markdown has, plus powerful logic
2. **Beginner-friendly** — no programming knowledge required
3. **Beautiful by default** — professional output with zero configuration
4. **RTL-first for Persian/Arabic** — built-in bidirectional text support
5. **Extensible** — plugin system, custom renderers, IDE integration

---

## 📅 Release Timeline

```
v0.6.0 ──────► v0.7.0 ──────► v0.8.0 ──────► v0.9.0 ──────► v1.0.0
 (now)        (Q1 2025)      (Q2 2025)       (Q3 2025)     (Q4 2025)
   ✅             🚧              📋              📋            🎯
```

| Version | Status | Target | Focus |
|---------|--------|--------|-------|
| v0.6.0 | ✅ Released | Jan 2025 | Rich features |
| v0.7.0 | 🚧 In Progress | Feb 2025 | Interactive elements |
| v0.8.0 | 📋 Planned | Apr 2025 | Export formats |
| v0.9.0 | 📋 Planned | Jul 2025 | Performance & plugins |
| v1.0.0 | 🎯 Vision | Oct 2025 | Stability & IDE |
| v1.1+ | 💭 Future | 2026+ | Ecosystem |

---

## 🚧 v0.7.0 — Interactive Elements

**Target:** February 2025
**Theme:** *"Make it interactive"*

### Core Features

- [ ] **`@run` directive** — Execute HTML/JS/CSS in-place
  ```mup
  @run {lang="html"}
  <button onclick="alert('Hi')">Click</button>
  @end
  ```
  - Sandboxed iframe execution
  - Error display
  - Console output capture

- [ ] **Nested lists** — Full support for indentation
  ```mup
  - Item 1
    - Nested 1.1
    - Nested 1.2
  - Item 2
  ```

- [ ] **Table cell spanning**
  ```mup
  | Header 1 | Header 2 |
  |----------|----------|
  | Cell {colspan=2}    |
  ```

- [ ] **Table cell types**
  - Markdown cell (default)
  - Code cell
  - Chart cell
  - Image cell

### Enhancements

- [ ] **Better error messages** with line context
  ```
  Error at line 42, column 8:
     42 │ @if x == 
        │         ↑ unexpected end of expression
  ```

- [ ] **Auto-fix suggestions**
  ```
  Unknown directive '@noet'. Did you mean '@note'?
  ```

- [ ] **Watch mode** (`mup watch file.mup`)
  - Auto-rebuild on file change
  - Browser auto-reload

- [ ] **Multi-file watch** (`mup watch docs/*.mup`)

### Documentation

- [ ] Add `@run` to `GUIDE.md`
- [ ] Add nested list examples
- [ ] Add table spanning examples
- [ ] Video tutorial (YouTube)

---

## 📋 v0.8.0 — Export Formats

**Target:** April 2025
**Theme:** *"Beyond HTML"*

### Export Formats

- [ ] **PDF export** (`mup file.mup --pdf`)
  - Print-friendly CSS
  - Page breaks
  - Table of contents

- [ ] **Markdown export** (`mup file.mup --md`)
  - Convert back to Markdown
  - Lossy (loses variables/logic)

- [ ] **EPUB export** (`mup book.mup --epub`)
  - For e-books
  - Chapter splitting

- [ ] **JSON export** (`mup file.mup --json`)
  - AST as JSON
  - For integrations

- [ ] **Static site generation** (`mup build docs/`)
  - Multiple `.mup` → multiple `.html`
  - Shared layout
  - Auto-linking

### Import Features

- [ ] **`@import` with variables**
  ```mup
  @import "card.mup" {title="Hello", body="World"}
  ```

- [ ] **`@include` for raw text**
  ```mup
  @include "code.py"
  ```

- [ ] **External data sources**
  ```mup
  @let data = @json("data.json")
  @let rows = @csv("sales.csv")
  ```

### Templates

- [ ] **Custom HTML templates**
  - Override default
  - Template variables
  - Partials

- [ ] **Theme marketplace**
  - Share themes
  - Install: `mup theme install <name>`

---

## 📋 v0.9.0 — Performance & Plugins

**Target:** July 2025
**Theme:** *"Fast and extensible"*

### Performance

- [ ] **Incremental compilation**
  - Only rebuild changed parts
  - Cache parsed ASTs

- [ ] **Streaming parser** for large files
  - Handle multi-GB files
  - Low memory footprint

- [ ] **Parallel rendering** (multiprocessing)
  - Speed up large documents

- [ ] **Lazy loading of charts and math**
  - Only render when scrolled to
  - Reduce initial load time

### Plugin System

- [ ] **Plugin API**
  ```python
  from markup_plus.plugin import Plugin

  class MyPlugin(Plugin):
      name = "my-plugin"
      version = "1.0.0"

      def register(self, registry):
          registry.add_directive("myblock", self.parse_myblock)
          registry.add_renderer("myblock", self.render_myblock)
  ```

- [ ] **Plugin discovery**
  - Entry points
  - Auto-load from `~/.markup-plus/plugins/`

- [ ] **Built-in plugins**
  - `markup-plus-emoji` — Emoji shortcodes
  - `markup-plus-diagrams` — Mermaid diagrams
  - `markup-plus-maps` — Interactive maps
  - `markup-plus-syntax` — Custom syntax themes

### Advanced Features

- [ ] **Regex-based replacements**
  ```mup
  @replace pattern="/TODO: (\w+)/g" text="Issue: $1"
  ```

- [ ] **Custom directives**
  ```mup
  @custom "my-directive" handler="my_handler"
  ```

- [ ] **Snippets**
  ```mup
  @snippet "warn" 
  @warning
  {content}
  @end
  @end

  @warn{content="Careful!"}
  ```

---

## 🎯 v1.0.0 — Stability & IDE

**Target:** October 2025
**Theme:** *"Ready for everyone"*

### Stability

- [ ] **API frozen** — no breaking changes until v2.0.0
- [ ] **100% test coverage** on core modules
- [ ] **Comprehensive benchmarks**
- [ ] **Security audit**
- [ ] **Performance guarantees** (e.g., 10k-line doc in <1s)

### Desktop IDE

- [ ] **Markup+ Studio** — cross-platform desktop app
  - Editor with syntax highlighting
  - Live preview (side-by-side)
  - File tree sidebar
  - Export buttons
  - Theme switcher
  - Built-in terminal
  - Component snippets
  - Error panel

- [ ] **Technology:** PyQt6 or Tauri
- [ ] **Platforms:** Windows, macOS, Linux
- [ ] **Size:** <50 MB installer

### Windows Installer

- [ ] **One-click installer** (`MarkupPlus-Setup-1.0.0.exe`)
  - Welcome screen
  - Install location picker
  - Components: Core, CLI, IDE, Docs
  - Add to PATH
  - File association (`.mup`)
  - Desktop shortcut
  - Uninstaller

- [ ] **Technology:** Inno Setup
- [ ] **Multi-language:** English, Persian, Arabic

### Documentation

- [ ] **Documentation website** (docs.markupplus.dev)
  - Search
  - Versioned docs
  - Interactive examples
  - Playground

- [ ] **Video course** (YouTube)
  - Getting started
  - Advanced features
  - Real-world projects

- [ ] **Book** (PDF, EPUB)
  - "Learning Markup+"

### Community

- [ ] **Discord server**
- [ ] **Discussion forum**
- [ ] **Monthly newsletter**
- [ ] **Showcase gallery**

---

## 💭 v1.1+ — The Future

**Target:** 2026+

### Integrations

- [ ] **VS Code extension**
  - Syntax highlighting
  - Live preview
  - Snippets
  - Error checking

- [ ] **JetBrains plugin**
  - IntelliJ, PyCharm, WebStorm

- [ ] **Vim/Neovim plugin**
- [ ] **Sublime Text package**
- [ ] **Atom package** (if still alive)

### Cloud Features

- [ ] **Online editor** (editor.markupplus.dev)
  - No installation
  - Share links
  - Collaboration
  - Version history

- [ ] **Cloud sync**
  - Save to cloud
  - Access anywhere

- [ ] **Publishing platform** (markupplus.dev)
  - Publish directly
  - Custom domains
  - Analytics

### AI Features

- [ ] **AI writing assistant**
  - Suggest completions
  - Fix grammar
  - Translate

- [ ] **AI-generated charts**
  ```mup
  @chart-ai
  Show me last quarter's sales
  @end
  ```

- [ ] **AI documentation**
  - Auto-generate docs from code

### Advanced Rendering

- [ ] **3D graphics** (Three.js)
- [ ] **Interactive diagrams** (Mermaid, D3.js)
- [ ] **Animated transitions**
- [ ] **Dark mode auto-scheduling**
- [ ] **Accessibility improvements** (WCAG 2.1 AA)

### Enterprise

- [ ] **Team collaboration**
- [ ] **Private registries**
- [ ] **SSO integration**
- [ ] **Audit logs**
- [ ] **On-premise deployment**

---

## 🎨 Feature Requests

Want a feature not on this list? [Open an issue!](https://github.com/USERNAME/markup-plus/issues/new?template=feature_request.md)

**Currently considering:**

- [ ] Video embeds (`@video`)
- [ ] Audio embeds (`@audio`)
- [ ] Interactive forms (`@form`)
- [ ] Database queries (`@query`)
- [ ] Real-time collaboration
- [ ] Version control integration
- [ ] REST API
- [ ] GraphQL support

---

## 📊 Prioritization Criteria

Features are prioritized by:

| Factor | Weight | Description |
|--------|:------:|-------------|
| **User demand** | 40% | Number of requests |
| **Impact** | 25% | How many users benefit |
| **Effort** | 20% | Implementation complexity |
| **Alignment** | 15% | Matches project vision |

Low-impact features with high effort are deprioritized.

---

## 🚫 Out of Scope

These are **not planned** for Markup+:

- ❌ **General-purpose programming** — use Python/JS
- ❌ **Server-side logic** — use a web framework
- ❌ **Database ORM** — use SQLAlchemy
- ❌ **Full CMS** — use WordPress/Strapi
- ❌ **Real-time apps** — use React/Vue
- ❌ **Mobile apps** — use React Native/Flutter

Markup+ stays focused on **static document generation** and **content markup**.

---

## 🤝 How to Influence the Roadmap

1. **Vote on issues** — 👍 reactions count
2. **Open feature requests** — with use cases
3. **Contribute code** — implement and submit PR
4. **Sponsor** — financial support speeds things up
5. **Spread the word** — more users = more priority

---

## 📅 Milestone Tracking

See live progress on [GitHub Milestones](https://github.com/USERNAME/markup-plus/milestones):

- [v0.7.0](https://github.com/USERNAME/markup-plus/milestone/1) — Interactive Elements
- [v0.8.0](https://github.com/USERNAME/markup-plus/milestone/2) — Export Formats
- [v0.9.0](https://github.com/USERNAME/markup-plus/milestone/3) — Performance & Plugins
- [v1.0.0](https://github.com/USERNAME/markup-plus/milestone/4) — Stability & IDE

---

## 💬 Discuss the Roadmap

Have thoughts? Join the discussion:

- 💬 [GitHub Discussions](https://github.com/USERNAME/markup-plus/discussions)
- 🐛 [Feature Requests](https://github.com/USERNAME/markup-plus/issues/new?template=feature_request.md)
- 📧 [Email](mailto:maintainer@markupplus.dev)

---

**Last updated:** January 2025
**Next review:** February 2025

---

> *"A roadmap is a promise to the future. But it's also a promise to the
> present — that we know where we're going."*
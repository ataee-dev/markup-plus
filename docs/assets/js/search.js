/* ============================================================
   Markup+ JS Documentation
   Client-Side Search
   ============================================================ */

(function () {
  'use strict';

  /* ==========================================================
     Search Index
     Each entry: { title, url, category, description, keywords }
     ========================================================== */

  const SEARCH_INDEX = [
    // --- Getting Started ---
    {
      title: 'Introduction',
      url: '/guides/getting-started.html',
      category: 'Getting Started',
      description:
        'What is Markup+? Learn about the modern markup language that extends Markdown.',
      keywords: 'intro overview what is markup plus',
    },
    {
      title: 'Installation',
      url: '/guides/installation.html',
      category: 'Getting Started',
      description:
        'Install Markup+ JS via npm, CDN, or from source. Node.js 18+ required.',
      keywords: 'install npm cdn setup nodejs yarn pnpm',
    },
    {
      title: 'CDN Usage',
      url: '/guides/cdn-usage.html',
      category: 'Getting Started',
      description:
        'Use Markup+ directly in the browser via jsDelivr or unpkg CDN.',
      keywords: 'cdn browser jsdelivr unpkg script tag',
    },

    // --- Examples ---
    {
      title: 'Basics',
      url: '/examples/01-basics.html',
      category: 'Examples',
      description: 'Get started with Markup+ basics: headings, paragraphs, bold, italic.',
      keywords: 'basic heading paragraph bold italic text format',
    },
    {
      title: 'Syntax',
      url: '/examples/02-syntax.html',
      category: 'Examples',
      description: 'Complete Markup+ syntax reference: everything you can write.',
      keywords: 'syntax reference cheat sheet grammar',
    },
    {
      title: 'Variables',
      url: '/examples/03-variables.html',
      category: 'Examples',
      description: 'Define variables with @let and use them with {name}. Filters included.',
      keywords: 'variable let define filter upper lower capitalize',
    },
    {
      title: 'Conditionals',
      url: '/examples/04-conditionals.html',
      category: 'Examples',
      description: 'Conditional content with @if, @elif, @else, @endif.',
      keywords: 'conditional if else elif logic condition',
    },
    {
      title: 'Loops',
      url: '/examples/05-loops.html',
      category: 'Examples',
      description: 'Iterate over arrays with @each and optional index.',
      keywords: 'loop each iterate array repeat for',
    },
    {
      title: 'Components',
      url: '/examples/06-components.html',
      category: 'Examples',
      description: 'Reusable components with @def and @Name(...).',
      keywords: 'component def reusable template function',
    },
    {
      title: 'Code Blocks',
      url: '/examples/07-code.html',
      category: 'Examples',
      description: 'Fenced code blocks with syntax highlighting, line numbers, titles.',
      keywords: 'code block fenced syntax highlight prism',
    },
    {
      title: 'Tables',
      url: '/examples/08-tables.html',
      category: 'Examples',
      description: 'Markdown-style tables with left, center, right alignment.',
      keywords: 'table grid row column align',
    },
    {
      title: 'Alerts',
      url: '/examples/09-alerts.html',
      category: 'Examples',
      description: 'Alert boxes: @note, @warning, @tip, @danger, @success.',
      keywords: 'alert note warning tip danger success callout admonition',
    },
    {
      title: 'Tabs & Collapse',
      url: '/examples/10-tabs-collapse.html',
      category: 'Examples',
      description: 'Tab groups and collapsible accordion sections.',
      keywords: 'tab tabs collapse accordion collapsible',
    },
    {
      title: 'Math',
      url: '/examples/11-math.html',
      category: 'Examples',
      description: 'Mathematical formulas with KaTeX — inline and block.',
      keywords: 'math katex formula latex equation',
    },
    {
      title: 'Charts',
      url: '/examples/12-charts.html',
      category: 'Examples',
      description: 'Bar, line, pie, and doughnut charts with Chart.js.',
      keywords: 'chart bar line pie doughnut graph chartjs',
    },
    {
      title: 'Gallery',
      url: '/examples/13-gallery.html',
      category: 'Examples',
      description: 'Image galleries with lightbox and keyboard navigation.',
      keywords: 'gallery image grid lightbox photo',
    },
    {
      title: 'RTL Support',
      url: '/examples/14-rtl.html',
      category: 'Examples',
      description: 'Automatic RTL detection for Persian, Arabic, Hebrew, Urdu.',
      keywords: 'rtl ltr right-to-left persian arabic hebrew urdu',
    },
    {
      title: 'Themes',
      url: '/examples/15-themes.html',
      category: 'Examples',
      description: '12 built-in themes plus custom CSS support.',
      keywords: 'theme dark light dracula nord catppuccin custom css',
    },
    {
      title: 'Fragment Rendering',
      url: '/examples/16-fragment.html',
      category: 'Examples',
      description: 'renderFragment for chatbots and embedded contexts.',
      keywords: 'fragment embed chatbot inline render',
    },
    {
      title: 'TypeScript',
      url: '/examples/17-typescript.html',
      category: 'Examples',
      description: 'Full TypeScript definitions for the public API.',
      keywords: 'typescript types definitions intellisense',
    },
    {
      title: 'CLI',
      url: '/examples/18-cli.html',
      category: 'Examples',
      description: 'Command-line interface: convert, watch, init, check.',
      keywords: 'cli command line mup-js terminal watch new init',
    },

    // --- Guides ---
    {
      title: 'CLI Reference',
      url: '/guides/cli-reference.html',
      category: 'Guides',
      description: 'Complete mup-js command-line reference with examples.',
      keywords: 'cli reference mup-js command options flags',
    },
    {
      title: 'JavaScript API',
      url: '/guides/javascript-api.html',
      category: 'Guides',
      description: 'Complete JS API: toHTML, toHTMLAsync, renderBody, renderFragment, parse.',
      keywords: 'api javascript js tohtml renderbody renderfragment parse',
    },
    {
      title: 'Python API',
      url: '/guides/python-api.html',
      category: 'Guides',
      description: 'Python equivalent of the Markup+ API.',
      keywords: 'python api pip markup-plus python to_html',
    },
    {
      title: 'Themes Guide',
      url: '/guides/themes.html',
      category: 'Guides',
      description: 'All 12 built-in themes with examples and custom CSS.',
      keywords: 'theme custom css style colors',
    },
    {
      title: 'RTL Guide',
      url: '/guides/rtl.html',
      category: 'Guides',
      description: 'Right-to-left language support and detection.',
      keywords: 'rtl right to left direction persian arabic',
    },
    {
      title: 'TypeScript Guide',
      url: '/guides/typescript.html',
      category: 'Guides',
      description: 'Using Markup+ JS with TypeScript.',
      keywords: 'typescript ts types type safety',
    },
    {
      title: 'Building a Chatbot',
      url: '/guides/chatbot.html',
      category: 'Guides',
      description: 'Build a chatbot that renders Markup+ responses.',
      keywords: 'chatbot chat fragment embed interactive',
    },
    {
      title: 'Migrating from Markdown',
      url: '/guides/migration.html',
      category: 'Guides',
      description: 'Switch from Markdown to Markup+ incrementally.',
      keywords: 'migrate markdown migration transition',
    },
    {
      title: 'VS Code Setup',
      url: '/guides/vs-code.html',
      category: 'Guides',
      description: 'Recommended VS Code extensions and settings.',
      keywords: 'vscode editor ide setup extension',
    },

    // --- Tools ---
    {
      title: 'Playground',
      url: '/playground/index.html',
      category: 'Tools',
      description: 'Online Markup+ editor with live preview.',
      keywords: 'playground editor online ide live preview',
    },
  ];

  /* ==========================================================
     Search Modal DOM
     ========================================================== */

  function createSearchModal() {
    const modal = document.createElement('div');
    modal.id = 'searchModal';
    modal.className = 'search-modal';
    modal.innerHTML = `
      <div class="search-modal-backdrop"></div>
      <div class="search-modal-box" role="dialog" aria-label="Search documentation">
        <div class="search-modal-header">
          <svg class="search-modal-icon" viewBox="0 0 24 24" width="20" height="20">
            <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2"/>
            <line x1="16" y1="16" x2="21" y2="21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <input
            type="text"
            id="searchInput"
            class="search-modal-input"
            placeholder="Search documentation..."
            autocomplete="off"
            spellcheck="false"
          >
          <kbd class="search-modal-kbd">Esc</kbd>
        </div>
        <div class="search-modal-results" id="searchResults"></div>
        <div class="search-modal-footer">
          <span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span>
          <span><kbd>Enter</kbd> Open</span>
          <span><kbd>Esc</kbd> Close</span>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  /* ==========================================================
     Search Styles (injected)
     ========================================================== */

  function injectSearchStyles() {
    if (document.getElementById('search-styles')) return;

    const style = document.createElement('style');
    style.id = 'search-styles';
    style.textContent = `
      .search-modal {
        position: fixed;
        inset: 0;
        z-index: 9999;
        display: none;
      }

      .search-modal.open {
        display: block;
        animation: searchFade 0.15s ease;
      }

      @keyframes searchFade {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      .search-modal-backdrop {
        position: absolute;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
      }

      .search-modal-box {
        position: relative;
        max-width: 600px;
        margin: 80px auto;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 14px;
        box-shadow: var(--shadow-lg);
        overflow: hidden;
        animation: searchSlide 0.2s ease;
      }

      @keyframes searchSlide {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }

      .search-modal-header {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 18px;
        border-bottom: 1px solid var(--border);
      }

      .search-modal-icon {
        color: var(--muted);
        flex-shrink: 0;
      }

      .search-modal-input {
        flex: 1;
        border: none;
        outline: none;
        background: transparent;
        font-size: 16px;
        font-family: inherit;
        color: var(--text);
      }

      .search-modal-input::placeholder {
        color: var(--muted);
      }

      .search-modal-kbd {
        padding: 3px 8px;
        background: var(--bg-alt);
        border: 1px solid var(--border);
        border-radius: 5px;
        font-size: 10px;
        font-weight: 600;
        color: var(--muted);
        font-family: 'JetBrains Mono', monospace;
      }

      .search-modal-results {
        max-height: 400px;
        overflow-y: auto;
        padding: 8px;
      }

      .search-result {
        display: block;
        padding: 12px 14px;
        border-radius: 8px;
        text-decoration: none;
        color: var(--text);
        cursor: pointer;
        transition: background 0.1s;
        border: 1px solid transparent;
      }

      .search-result:hover,
      .search-result.selected {
        background: var(--bg-alt);
        border-color: var(--border);
      }

      .search-result.selected {
        border-color: var(--primary);
      }

      .search-result-category {
        display: inline-block;
        padding: 2px 8px;
        background: var(--primary);
        color: white;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        margin-bottom: 6px;
      }

      .search-result-title {
        font-weight: 600;
        font-size: 14px;
        color: var(--text);
        margin-bottom: 3px;
      }

      .search-result-title mark {
        background: rgba(102, 126, 234, 0.25);
        color: var(--primary);
        padding: 0 2px;
        border-radius: 2px;
      }

      .search-result-description {
        font-size: 12.5px;
        color: var(--muted);
        line-height: 1.5;
      }

      .search-empty {
        padding: 40px 20px;
        text-align: center;
        color: var(--muted);
        font-size: 14px;
      }

      .search-empty-icon {
        font-size: 40px;
        margin-bottom: 12px;
        opacity: 0.4;
      }

      .search-modal-footer {
        display: flex;
        gap: 16px;
        padding: 10px 18px;
        border-top: 1px solid var(--border);
        background: var(--bg-alt);
        font-size: 11px;
        color: var(--muted);
      }

      .search-modal-footer kbd {
        padding: 2px 6px;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 4px;
        font-size: 10px;
        font-family: 'JetBrains Mono', monospace;
      }

      @media (max-width: 700px) {
        .search-modal-box {
          margin: 40px 16px;
          max-width: none;
        }

        .search-modal-results {
          max-height: 60vh;
        }
      }
    `;
    document.head.appendChild(style);
  }

  /* ==========================================================
     Search Logic
     ========================================================== */

  function normalize(str) {
    return (str || '').toLowerCase().trim();
  }

  function scoreEntry(entry, query) {
    const q = normalize(query);
    if (!q) return 0;

    const title = normalize(entry.title);
    const desc = normalize(entry.description);
    const keywords = normalize(entry.keywords);
    const category = normalize(entry.category);

    let score = 0;

    // Exact title match
    if (title === q) score += 100;
    // Title starts with query
    else if (title.startsWith(q)) score += 50;
    // Title contains query
    else if (title.includes(q)) score += 30;

    // Keywords match
    if (keywords.includes(q)) score += 20;

    // Category match
    if (category.includes(q)) score += 10;

    // Description match
    if (desc.includes(q)) score += 5;

    // Multi-word: all words must match somewhere
    const words = q.split(/\s+/).filter(Boolean);
    if (words.length > 1) {
      const haystack = title + ' ' + desc + ' ' + keywords + ' ' + category;
      const allMatch = words.every((w) => haystack.includes(w));
      if (!allMatch) return 0;
      score += 5;
    }

    return score;
  }

  function search(query) {
    if (!query || !query.trim()) return [];

    return SEARCH_INDEX.map((entry) => ({
      entry,
      score: scoreEntry(entry, query),
    }))
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 12)
      .map((r) => r.entry);
  }

  function highlight(text, query) {
    if (!query) return text;
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp('(' + escaped + ')', 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }

  function renderResults(results, query) {
    const container = document.getElementById('searchResults');
    if (!container) return;

    if (results.length === 0) {
      container.innerHTML = `
        <div class="search-empty">
          <div class="search-empty-icon">🔍</div>
          <div>No results for "<strong>${escapeHtml(query)}</strong>"</div>
          <div style="margin-top:8px;font-size:12px;">Try different keywords</div>
        </div>
      `;
      return;
    }

    container.innerHTML = results
      .map(
        (r, i) => `
        <a class="search-result" href="${r.url}" data-index="${i}">
          <div class="search-result-category">${escapeHtml(r.category)}</div>
          <div class="search-result-title">${highlight(escapeHtml(r.title), query)}</div>
          <div class="search-result-description">${escapeHtml(r.description)}</div>
        </a>
      `
      )
      .join('');

    container.querySelectorAll('.search-result').forEach((el) => {
      el.addEventListener('click', closeSearch);
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  /* ==========================================================
     Modal Control
     ========================================================== */

  let searchModal = null;
  let searchInput = null;
  let currentResults = [];
  let selectedIndex = 0;

  function openSearch() {
    if (!searchModal) return;
    searchModal.classList.add('open');
    document.body.style.overflow = 'hidden';

    setTimeout(() => {
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }, 50);

    // Initial empty state
    const container = document.getElementById('searchResults');
    if (container && !container.innerHTML.trim()) {
      container.innerHTML = `
        <div class="search-empty">
          <div class="search-empty-icon">📚</div>
          <div>Start typing to search the documentation</div>
          <div style="margin-top:12px;font-size:12px;color:var(--muted-2);">
            Try: <strong>variables</strong>, <strong>charts</strong>, <strong>CLI</strong>, <strong>RTL</strong>
          </div>
        </div>
      `;
    }
  }

  function closeSearch() {
    if (!searchModal) return;
    searchModal.classList.remove('open');
    document.body.style.overflow = '';
    if (searchInput) searchInput.value = '';
  }

  function handleSearchInput(e) {
    const query = e.target.value;
    currentResults = search(query);
    selectedIndex = 0;
    renderResults(currentResults, query);
  }

  function handleKeydown(e) {
    // Ctrl/Cmd + K → open
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
      return;
    }

    // If modal is closed, ignore
    if (!searchModal || !searchModal.classList.contains('open')) return;

    // Escape → close
    if (e.key === 'Escape') {
      e.preventDefault();
      closeSearch();
      return;
    }

    // Arrow navigation
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (currentResults.length === 0) return;
      selectedIndex = Math.min(selectedIndex + 1, currentResults.length - 1);
      updateSelection();
      return;
    }

    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (currentResults.length === 0) return;
      selectedIndex = Math.max(selectedIndex - 1, 0);
      updateSelection();
      return;
    }

    // Enter → open selected
    if (e.key === 'Enter') {
      e.preventDefault();
      if (currentResults[selectedIndex]) {
        window.location.href = currentResults[selectedIndex].url;
      }
    }
  }

  function updateSelection() {
    const results = document.querySelectorAll('.search-result');
    results.forEach((el, i) => {
      el.classList.toggle('selected', i === selectedIndex);
      if (i === selectedIndex) {
        el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    });
  }

  /* ==========================================================
     Init
     ========================================================== */

  function init() {
    injectSearchStyles();

    searchModal = createSearchModal();
    searchInput = document.getElementById('searchInput');

    const backdrop = searchModal.querySelector('.search-modal-backdrop');
    if (backdrop) backdrop.addEventListener('click', closeSearch);

    if (searchInput) {
      searchInput.addEventListener('input', handleSearchInput);
    }

    document.addEventListener('keydown', handleKeydown);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* ==========================================================
     Expose API
     ========================================================== */

  window.MarkupSearch = {
    open: openSearch,
    close: closeSearch,
    search: search,
  };
})();
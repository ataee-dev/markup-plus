/* ============================================================
   Markup+ JS Documentation
   Main Script
   ============================================================ */

(function () {
  'use strict';

  /* ==========================================================
     1. Theme Management
     ========================================================== */

  const THEME_KEY = 'markup-plus-docs-theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === 'light' || stored === 'dark') return stored;

    return window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);

    const toggle = document.getElementById('themeToggle');
    if (toggle) {
      toggle.textContent = theme === 'dark' ? '☀' : '☾';
      toggle.setAttribute(
        'aria-label',
        theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
      );
    }
  }

  function initTheme() {
    setTheme(getPreferredTheme());

    const toggle = document.getElementById('themeToggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    // Listen to system changes
    window
      .matchMedia('(prefers-color-scheme: dark)')
      .addEventListener('change', (e) => {
        if (!localStorage.getItem(THEME_KEY)) {
          setTheme(e.matches ? 'dark' : 'light');
        }
      });
  }

  /* ==========================================================
     2. Mobile Sidebar
     ========================================================== */

  function initMobileMenu() {
    const button = document.getElementById('menuButton');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    if (!button || !sidebar) return;

    function open() {
      sidebar.classList.add('open');
      if (overlay) overlay.classList.add('show');
      document.body.style.overflow = 'hidden';
    }

    function close() {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('show');
      document.body.style.overflow = '';
    }

    button.addEventListener('click', open);
    if (overlay) overlay.addEventListener('click', close);

    sidebar.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', close);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) close();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') close();
    });
  }

  /* ==========================================================
     3. Active Nav Link
     ========================================================== */

  function markActiveNavLink() {
    const path = window.location.pathname.replace(/\/$/, '').toLowerCase();
    const currentFile = path.split('/').pop() || 'index.html';

    document.querySelectorAll('.nav-section a').forEach((link) => {
      const href = (link.getAttribute('href') || '').toLowerCase();
      if (!href || href.startsWith('http')) return;

      const linkFile = href.split('/').pop();

      if (linkFile === currentFile) {
        link.classList.add('active');
      }
    });
  }

  /* ==========================================================
     4. Table of Contents
     ========================================================== */

  function slugify(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[^\w\s\u0600-\u06FF-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '') || 'section';
  }

  function buildTOC() {
    const tocList = document.getElementById('toc-list');
    const toc = document.getElementById('toc');
    if (!tocList || !toc) return;

    const article = document.querySelector('.article');
    if (!article) {
      toc.style.display = 'none';
      return;
    }

    const headings = article.querySelectorAll('h2, h3');
    if (headings.length === 0) {
      toc.style.display = 'none';
      return;
    }

    headings.forEach((heading) => {
      if (!heading.id) {
        heading.id = slugify(heading.textContent);
      }

      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + heading.id;
      a.textContent = heading.textContent;

      if (heading.tagName === 'H3') a.classList.add('h3');

      li.appendChild(a);
      tocList.appendChild(li);
    });

    // Active link on scroll
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            document.querySelectorAll('.toc a').forEach((link) => {
              link.classList.toggle(
                'active',
                link.getAttribute('href') === '#' + id
              );
            });
          }
        });
      },
      {
        rootMargin: '-80px 0px -70% 0px',
        threshold: 0,
      }
    );

    headings.forEach((h) => observer.observe(h));
  }

  /* ==========================================================
     5. Example Tabs
     ========================================================== */

  function initExampleTabs() {
    document.querySelectorAll('.example').forEach((example) => {
      const tabs = example.querySelectorAll('.example-tab');
      const panels = example.querySelectorAll('.example-panel');

      tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
          const target = tab.dataset.panel;

          tabs.forEach((t) => t.classList.remove('active'));
          panels.forEach((p) => p.classList.remove('active'));

          tab.classList.add('active');
          const panel = example.querySelector(
            `.example-panel[data-panel="${target}"]`
          );
          if (panel) panel.classList.add('active');

          // Re-highlight prism when showing code panel
          if (
            target === 'mup' ||
            target === 'html' ||
            target === 'js'
          ) {
            if (window.Prism) {
              window.Prism.highlightAllUnder(panel);
            }
          }
        });
      });
    });
  }

  /* ==========================================================
     6. Copy Code Buttons
     ========================================================== */

  const COPY_ICON = `
    <svg viewBox="0 0 24 24">
      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
  `;

  const CHECK_ICON = `
    <svg viewBox="0 0 24 24">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  `;

  function initCopyButtons() {
    const selector = '.article pre, .example-code';
    document.querySelectorAll(selector).forEach((pre) => {
      if (pre.querySelector('.copy-button, .code-copy')) return;

      const button = document.createElement('button');
      button.className = 'copy-button';
      button.setAttribute('aria-label', 'Copy code');
      button.innerHTML = COPY_ICON;

      button.addEventListener('click', async (e) => {
        e.stopPropagation();
        const code = pre.querySelector('code');
        if (!code) return;

        try {
          await navigator.clipboard.writeText(code.textContent);
          button.innerHTML = CHECK_ICON;
          button.classList.add('copied');

          setTimeout(() => {
            button.innerHTML = COPY_ICON;
            button.classList.remove('copied');
          }, 2000);
        } catch (err) {
          console.error('Copy failed:', err);
          // Fallback
          const textarea = document.createElement('textarea');
          textarea.value = code.textContent;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          document.body.appendChild(textarea);
          textarea.select();
          try {
            document.execCommand('copy');
            button.innerHTML = CHECK_ICON;
            button.classList.add('copied');
            setTimeout(() => {
              button.innerHTML = COPY_ICON;
              button.classList.remove('copied');
            }, 2000);
          } catch (e2) {
            console.error('Fallback copy failed', e2);
          }
          document.body.removeChild(textarea);
        }
      });

      pre.style.position = 'relative';
      pre.appendChild(button);
    });
  }

  /* ==========================================================
     7. Smooth Scroll for Anchors
     ========================================================== */

  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((link) => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (!href || href === '#' || href.length < 2) return;

        const target = document.querySelector(href);
        if (!target) return;

        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        history.pushState(null, '', href);
      });
    });
  }

  /* ==========================================================
     8. Keyboard Shortcuts
     ========================================================== */

  function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl/Cmd + K → Search (disabled for now)
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) searchInput.focus();
      }

      // Escape → close mobile sidebar
      if (e.key === 'Escape') {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        if (sidebar) sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('show');
        document.body.style.overflow = '';
      }
    });
  }

  /* ==========================================================
     9. Auto-detect Theme for Examples
     ========================================================== */

  function initExamplePreviews() {
    document.querySelectorAll('[data-mup]').forEach((el) => {
      if (typeof window.MarkupPlus === 'undefined') {
        console.warn('MarkupPlus not loaded');
        return;
      }

      try {
        const source = el.getAttribute('data-mup');
        const mode = el.getAttribute('data-mode') || 'body';

        if (mode === 'body') {
          el.innerHTML = window.MarkupPlus.renderBody(source);
        } else if (mode === 'fragment') {
          el.innerHTML = window.MarkupPlus.renderFragment(source, {
            includeScripts: true,
            includeCDNScripts: true,
          });
        } else if (mode === 'full') {
          el.innerHTML = window.MarkupPlus.toHTML(source);
        }
      } catch (err) {
        el.innerHTML = `<div class="error-block">${err.message}</div>`;
      }
    });
  }

  /* ==========================================================
     10. Scroll Reveal Animation
     ========================================================== */

  function initScrollReveal() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
      }
    );

    document
      .querySelectorAll('.feature-card, .example, .callout')
      .forEach((el) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(16px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
      });
  }

  /* ==========================================================
     11. External Links
     ========================================================== */

  function initExternalLinks() {
    document.querySelectorAll('a[href^="http"]').forEach((link) => {
      const href = link.getAttribute('href');
      if (
        href.includes(window.location.hostname) ||
        href.startsWith('https://github.com/ataee-dev') ||
        href.startsWith('https://www.npmjs.com') ||
        href.startsWith('https://pypi.org')
      ) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
      }
    });
  }

  /* ==========================================================
     12. Reading Progress Bar
     ========================================================== */

  function initReadingProgress() {
    const article = document.querySelector('.article');
    if (!article) return;

    const bar = document.createElement('div');
    bar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      height: 3px;
      background: linear-gradient(90deg, #667eea, #ec4899);
      z-index: 9999;
      transition: width 0.1s ease;
      width: 0%;
      box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    `;
    document.body.appendChild(bar);

    function update() {
      const scrollTop = window.scrollY;
      const docHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const percent = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, percent)) + '%';
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ==========================================================
     13. Heading Anchors
     ========================================================== */

  function initHeadingAnchors() {
    document.querySelectorAll('.article h2, .article h3').forEach((h) => {
      if (!h.id) h.id = slugify(h.textContent);

      h.style.position = 'relative';

      const anchor = document.createElement('a');
      anchor.href = '#' + h.id;
      anchor.textContent = '#';
      anchor.style.cssText = `
        position: absolute;
        left: -24px;
        top: 50%;
        transform: translateY(-50%);
        opacity: 0;
        color: var(--primary);
        text-decoration: none;
        font-weight: 400;
        font-size: 0.8em;
        transition: opacity 0.2s;
      `;
      anchor.setAttribute('aria-label', 'Link to this section');

      h.addEventListener('mouseenter', () => {
        anchor.style.opacity = '1';
      });
      h.addEventListener('mouseleave', () => {
        anchor.style.opacity = '0';
      });

      h.appendChild(anchor);
    });
  }

  /* ==========================================================
     14. Init All
     ========================================================== */

  function init() {
    initTheme();
    initMobileMenu();
    markActiveNavLink();
    buildTOC();
    initExampleTabs();
    initCopyButtons();
    initSmoothScroll();
    initKeyboardShortcuts();
    initExamplePreviews();
    initScrollReveal();
    initExternalLinks();
    initReadingProgress();
    initHeadingAnchors();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
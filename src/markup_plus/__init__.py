"""
Markup+ — A modern markup language with more features than Markdown.

Features:
    - Markdown-compatible syntax
    - Variables, conditionals, loops
    - Reusable components
    - Charts (bar, line, pie, doughnut)
    - Math formulas (KaTeX)
    - Tabs, collapse, alerts, timeline
    - Auto RTL detection (Persian, Arabic, Hebrew)
    - Rich code blocks with copy/download/preview
    - Light/dark themes
"""

__version__ = "0.6.0"
__author__ = "Ataee"
__license__ = "MIT"

from .renderer import to_html
from .parser import parse_text

__all__ = ["to_html", "parse_text", "__version__"]
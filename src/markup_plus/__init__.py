"""
Markup+ — A modern markup language with more features than Markdown.
"""

__version__ = "0.1.0"
__author__ = "Ataee"
__license__ = "MIT"

from .renderer import to_html

__all__ = ["to_html", "__version__"]
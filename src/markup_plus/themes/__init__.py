"""
Theme loading for Markup+.

Handles both development mode and PyInstaller frozen mode.
"""

import sys
from pathlib import Path
from typing import Optional


def _get_themes_dir() -> Path:
    """
    Get the themes directory path.

    Handles two cases:
    1. Development: <project>/src/markup_plus/themes/css
    2. PyInstaller:  <exe_dir>/_internal/markup_plus/themes/css
    """
    # Case 1: PyInstaller frozen executable
    if getattr(sys, "frozen", False):
        # PyInstaller stores everything under sys._MEIPASS
        # In PyInstaller 6.x (one-dir), sys._MEIPASS = _internal dir
        base = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        candidates = [
            base / "markup_plus" / "themes" / "css",
            base / "_internal" / "markup_plus" / "themes" / "css",
            Path(sys.executable).parent / "_internal" / "markup_plus" / "themes" / "css",
            Path(sys.executable).parent / "markup_plus" / "themes" / "css",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        # Fallback: return first candidate (will fail gracefully)
        return candidates[0]

    # Case 2: Development mode
    return Path(__file__).parent / "css"


THEMES_DIR = _get_themes_dir()


def load_base_css() -> str:
    """Load the base stylesheet bundled with Markup+."""
    base = THEMES_DIR / "base.css"
    if base.exists():
        return base.read_text(encoding="utf-8")
    return ""


def load_custom_css(path: str) -> Optional[str]:
    """Load a custom CSS file."""
    css_path = Path(path)
    if not css_path.exists():
        return None
    if not css_path.is_file():
        return None
    try:
        return css_path.read_text(encoding="utf-8")
    except Exception:
        return None


def build_css(custom_path: Optional[str] = None) -> str:
    """Build the complete CSS for a document."""
    parts = [load_base_css()]

    if custom_path:
        custom = load_custom_css(custom_path)
        if custom:
            parts.append("")
            parts.append("/* ============================================================")
            parts.append("   Custom CSS (from user)")
            parts.append("   ============================================================ */")
            parts.append("")
            parts.append(custom)

    return "\n".join(parts)
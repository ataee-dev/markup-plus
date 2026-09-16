"""
CLI Display — View Markup+ files in terminal with syntax highlighting.
"""

import re
from pathlib import Path

from . import theme


# ============================================================
# Token definitions for .mup syntax
# ============================================================

MUP_PATTERNS = [
    # Order matters — most specific first
    ("heading",     re.compile(r"^#{1,6}\s+.+$")),
    ("directive",   re.compile(r"^@\w+.*$")),
    ("math",        re.compile(r"^\$\$.*\$\$$")),
    ("hr",          re.compile(r"^[-*_]{3,}\s*$")),
    ("table",       re.compile(r"^\|.*\|$")),
    ("image",       re.compile(r"^!\[.*?\]\(.*?\).*$")),
    ("variable",    re.compile(r"\{[a-zA-Z_]\w*(?:\s*\|\s*\w+)*\}")),
    ("bold",        re.compile(r"\*\*[^*]+\*\*")),
    ("italic",      re.compile(r"(?<!\*)\*[^*]+\*(?!\*)")),
    ("code_inline", re.compile(r"`[^`]+`")),
    ("link",        re.compile(r"\[[^\]]+\]\([^)]+\)")),
    ("comment",     re.compile(r"^@#.*$")),
    ("list",        re.compile(r"^\s*[-*+]\s+.+$")),
    ("olist",       re.compile(r"^\s*\d+\.\s+.+$")),
    ("quote",       re.compile(r"^\s*>\s?.+$")),
]

COLORS = {
    "heading":     (theme.bold, theme.magenta),
    "directive":   (theme.bold, theme.cyan),
    "math":        (theme.bold, theme.yellow),
    "hr":          (theme.dim,),
    "table":       (theme.blue,),
    "image":       (theme.green,),
    "variable":    (theme.yellow,),
    "bold":        (theme.bold,),
    "italic":      (theme.italic_display if hasattr(theme, "italic_display") else theme.dim,),
    "code_inline": (theme.bg_style if hasattr(theme, "bg_style") else theme.cyan,),
    "link":        (theme.blue, theme.underline_display if hasattr(theme, "underline_display") else theme.dim,),
    "comment":     (theme.dim,),
    "list":        (theme.green,),
    "olist":       (theme.green,),
    "quote":       (theme.yellow,),
}


# ============================================================
# Syntax highlighting
# ============================================================

def highlight_line(line: str) -> str:
    """Apply syntax highlighting to a single line."""
    if not theme.USE_COLOR:
        return line
    
    # Check patterns in order
    for name, pattern in MUP_PATTERNS:
        if pattern.search(line):
            colors = COLORS.get(name, ())
            # For headings, apply to entire line
            if name in ("heading", "hr", "table", "comment"):
                return theme.colorize(line, *colors)
            # For other patterns, apply inline
            break
    
    # Apply inline formatting
    line = _highlight_inline(line)
    return line


def _highlight_inline(line: str) -> str:
    """Apply inline highlighting (bold, italic, code, variables, links)."""
    if not theme.USE_COLOR:
        return line
    
    # Inline code
    line = re.sub(
        r"`([^`]+)`",
        lambda m: theme.colorize(f"`{m.group(1)}`", theme.cyan),
        line,
    )
    
    # Bold
    line = re.sub(
        r"\*\*([^*]+)\*\*",
        lambda m: theme.bold(m.group(0)),
        line,
    )
    
    # Italic
    line = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        lambda m: theme.dim(m.group(0)),
        line,
    )
    
    # Variables {var}
    line = re.sub(
        r"\{([a-zA-Z_]\w*(?:\s*\|\s*\w+)*)\}",
        lambda m: theme.yellow(m.group(0)),
        line,
    )
    
    # Links
    line = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: theme.blue(m.group(1)) + theme.dim("(" + m.group(2) + ")"),
        line,
    )
    
    return line


def highlight(text: str) -> str:
    """Apply syntax highlighting to entire text."""
    lines = text.split("\n")
    return "\n".join(highlight_line(line) for line in lines)


# ============================================================
# File viewer
# ============================================================

def view_file(file_path: Path, show_numbers: bool = True) -> None:
    """
    Display a Markup+ file in the terminal with syntax highlighting.
    """
    if not file_path.exists():
        from .errors import show_error
        show_error(f"File not found: {file_path}")
        return
    
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        from .errors import show_error
        show_error(f"File is not valid UTF-8: {file_path}")
        return
    
    lines = content.split("\n")
    
    # Header
    print()
    print(theme.header(f"📄 {file_path.name}"))
    print(theme.dim("─" * 60))
    print()
    
    # Content with line numbers
    max_num_width = len(str(len(lines)))
    
    for i, line in enumerate(lines, start=1):
        highlighted = highlight_line(line)
        
        if show_numbers:
            num = theme.dim(f"{i:>{max_num_width}}")
            print(f"  {num} │ {highlighted}")
        else:
            print(f"  {highlighted}")
    
    # Footer
    print()
    print(theme.dim("─" * 60))
    print(theme.dim(f"  {len(lines)} lines • {len(content)} chars"))
    print()
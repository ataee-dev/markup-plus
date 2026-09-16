"""
CLI Errors — Error display and debugging utilities.
"""

from pathlib import Path
from typing import Optional, List

from . import theme


# ============================================================
# Error display
# ============================================================

def show_error(message: str, line: int = 0, file: Optional[Path] = None) -> None:
    """Display an error message with formatting."""
    icon = theme.red("✖")
    label = theme.error("Error")
    
    print(f"\n{icon} {label}: {message}")
    
    if file:
        print(f"   {theme.dim('File:')} {theme.cyan(str(file))}")
    
    if line > 0:
        print(f"   {theme.dim('Line:')} {theme.yellow(str(line))}")
    
    print()


def show_warning(message: str, line: int = 0) -> None:
    """Display a warning message."""
    icon = theme.yellow("⚠")
    label = theme.warning("Warning")
    
    print(f"{icon} {label}: {message}")
    
    if line > 0:
        print(f"   {theme.dim('Line:')} {theme.yellow(str(line))}")


def show_success(message: str) -> None:
    """Display a success message."""
    icon = theme.green("✔")
    label = theme.success("OK")
    print(f"{icon} {label}: {message}")


def show_info(message: str) -> None:
    """Display an info message."""
    icon = theme.cyan("ℹ")
    label = theme.info("Info")
    print(f"{icon} {label}: {message}")


# ============================================================
# Source code display with line numbers
# ============================================================

def show_source_context(
    file: Path,
    line: int,
    context: int = 2,
) -> None:
    """
    Show the source code around an error with line numbers.
    
    Example:
        Error on line 5:
            3 │ # Some code
            4 │ x = 10
            5 │ undefined_var  ← ERROR HERE
            6 │ print(x)
    """
    try:
        lines = file.read_text(encoding="utf-8").split("\n")
    except Exception:
        return
    
    start = max(0, line - context - 1)
    end = min(len(lines), line + context)
    
    print()
    for i in range(start, end):
        line_num = i + 1
        content = lines[i] if i < len(lines) else ""
        
        # Line number
        num_str = f"{line_num:4d}"
        
        if line_num == line:
            # Error line — highlight
            marker = theme.red("→")
            num = theme.red(num_str)
            content_display = theme.red(content)
            print(f"   {marker} {num} │ {content_display}")
            print(f"        {theme.dim(' ' * 4)} │ {theme.red('↑ error here')}")
        else:
            num = theme.dim(num_str)
            content_display = theme.dim(content)
            print(f"     {num} │ {content_display}")
    print()


# ============================================================
# Debug mode
# ============================================================

def show_debug_info(data: dict) -> None:
    """Show debug information about a build."""
    print(theme.header("\n🐛 Debug Info"))
    print(theme.dim("─" * 50))
    
    for key, value in data.items():
        key_fmt = theme.cyan(f"{key}:")
        print(f"  {key_fmt} {value}")
    
    print(theme.dim("─" * 50))
    print()


# ============================================================
# Statistics
# ============================================================

def show_stats(stats: dict) -> None:
    """Show build statistics."""
    print(theme.header("\n📊 Statistics"))
    print(theme.dim("─" * 50))
    
    for key, value in stats.items():
        key_fmt = theme.cyan(f"{key}:")
        print(f"  {key_fmt} {theme.bold(str(value))}")
    
    print(theme.dim("─" * 50))
    print()
"""
CLI Theme — Colors and styling for terminal output.
"""

import os
import sys


# ============================================================
# ANSI Color Codes
# ============================================================

class Color:
    """ANSI color codes for terminal."""
    
    # Reset
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Foreground
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Bright foreground
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# ============================================================
# Terminal detection
# ============================================================

def supports_color() -> bool:
    """Check if terminal supports ANSI colors."""
    if os.getenv("NO_COLOR"):
        return False
    if os.getenv("FORCE_COLOR"):
        return True
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    if sys.platform == "win32":
        # Enable ANSI on Windows
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True


USE_COLOR = supports_color()


# ============================================================
# Colorize helpers
# ============================================================

def colorize(text: str, *codes: str) -> str:
    """Wrap text with ANSI codes."""
    if not USE_COLOR:
        return text
    return "".join(codes) + text + Color.RESET


def red(text: str) -> str:
    return colorize(text, Color.RED)


def green(text: str) -> str:
    return colorize(text, Color.GREEN)


def yellow(text: str) -> str:
    return colorize(text, Color.YELLOW)


def blue(text: str) -> str:
    return colorize(text, Color.BLUE)


def magenta(text: str) -> str:
    return colorize(text, Color.MAGENTA)


def cyan(text: str) -> str:
    return colorize(text, Color.CYAN)


def bold(text: str) -> str:
    return colorize(text, Color.BOLD)


def dim(text: str) -> str:
    return colorize(text, Color.DIM)


def success(text: str) -> str:
    return colorize(text, Color.BOLD, Color.GREEN)


def error(text: str) -> str:
    return colorize(text, Color.BOLD, Color.RED)


def warning(text: str) -> str:
    return colorize(text, Color.BOLD, Color.YELLOW)


def info(text: str) -> str:
    return colorize(text, Color.BOLD, Color.CYAN)


def header(text: str) -> str:
    return colorize(text, Color.BOLD, Color.BRIGHT_MAGENTA)
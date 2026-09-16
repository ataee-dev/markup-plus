"""
Markup+ CLI

Command-line entry point. Provides the `mup` command.
"""

import sys
from pathlib import Path

from . import __version__
from .renderer import to_html


HELP_TEXT = """Markup+ CLI

Usage:
    mup <file.mup> [options]        Convert file.mup to file.html
    mup build <file.mup> [options]  Same as above (explicit)
    mup --version                   Show version
    mup --help                      Show this help

Options:
    --light, -l    Use light theme (default)
    --dark, -d     Use dark theme
    --rtl          Force right-to-left layout (Persian, Arabic, Hebrew)
    --ltr          Force left-to-right layout
                   (default: auto-detect from content)

Examples:
    mup examples/hello.mup
    mup examples/gallery.mup --dark
    mup examples/test_fa.mup --rtl
"""


def main() -> int:
    args = sys.argv[1:]

    if not args:
        print(HELP_TEXT)
        return 0

    if args[0] in ("--version", "-v"):
        print(f"Markup+ v{__version__}")
        return 0

    if args[0] in ("--help", "-h"):
        print(HELP_TEXT)
        return 0

    theme = "light"
    direction = None
    filtered_args = []

    for arg in args:
        if arg in ("--dark", "-d"):
            theme = "dark"
        elif arg in ("--light", "-l"):
            theme = "light"
        elif arg == "--rtl":
            direction = "rtl"
        elif arg == "--ltr":
            direction = "ltr"
        else:
            filtered_args.append(arg)

    if filtered_args and filtered_args[0] == "build":
        if len(filtered_args) < 2:
            print("Error: 'build' requires a file argument")
            return 1
        return build_file(filtered_args[1], theme, direction)

    if filtered_args:
        return build_file(filtered_args[0], theme, direction)

    print(HELP_TEXT)
    return 0


def build_file(path_str: str, theme: str = "light", direction: str = None) -> int:
    input_file = Path(path_str)

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        return 1

    if input_file.suffix != ".mup":
        print(f"Warning: File does not have .mup extension: {input_file}")

    try:
        text = input_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Error: File is not valid UTF-8: {input_file}")
        return 1

    html = to_html(
        text,
        title=input_file.stem,
        theme=theme,
        direction=direction,
    )

    output_file = input_file.with_suffix(".html")
    try:
        output_file.write_text(html, encoding="utf-8")
    except OSError as e:
        print(f"Error: Could not write output: {e}")
        return 1

    theme_label = "dark" if theme == "dark" else "light"
    dir_label = direction or "auto"
    print(f"OK ({theme_label}, {dir_label}): {input_file} -> {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
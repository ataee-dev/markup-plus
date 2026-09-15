"""
Markup+ CLI

Command-line entry point. Provides the `mup` command.

Usage:
    mup <file.mup>            Convert file.mup to file.html
    mup build <file.mup>      Same as above (explicit)
    mup --version             Show version
    mup --help                Show help
"""

import sys
from pathlib import Path

from . import __version__
from .renderer import to_html


HELP_TEXT = """Markup+ CLI

Usage:
    mup <file.mup>            Convert file.mup to file.html
    mup build <file.mup>      Same as above (explicit)
    mup --version             Show version
    mup --help                Show this help

Examples:
    mup examples/hello.mup
    mup build docs/index.mup
"""


def main() -> int:
    """Main CLI entry point. Returns exit code."""
    args = sys.argv[1:]

    # No arguments
    if not args:
        print(HELP_TEXT)
        return 0

    # --version
    if args[0] in ("--version", "-v"):
        print(f"Markup+ v{__version__}")
        return 0

    # --help
    if args[0] in ("--help", "-h"):
        print(HELP_TEXT)
        return 0

    # mup build <file>
    if args[0] == "build":
        if len(args) < 2:
            print("Error: 'build' requires a file argument")
            print("Usage: mup build <file.mup>")
            return 1
        return build_file(args[1])

    # mup <file>
    return build_file(args[0])


def build_file(path_str: str) -> int:
    """Convert a .mup file to .html."""
    input_file = Path(path_str)

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        return 1

    if input_file.suffix != ".mup":
        print(f"Warning: File does not have .mup extension: {input_file}")

    # Read
    try:
        text = input_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Error: File is not valid UTF-8: {input_file}")
        return 1

    # Convert
    html = to_html(text, title=input_file.stem)

    # Write
    output_file = input_file.with_suffix(".html")
    try:
        output_file.write_text(html, encoding="utf-8")
    except OSError as e:
        print(f"Error: Could not write output: {e}")
        return 1

    print(f"OK: {input_file} -> {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
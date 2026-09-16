"""
Markup+ CLI — Command-line interface.

Provides the `mup` command.
"""

import sys

from . import theme
from .. import __version__


HELP_TEXT = """
╔══════════════════════════════════════════════════════════════╗
║                         Markup+                              ║
║           A modern markup language for everyone              ║
╚══════════════════════════════════════════════════════════════╝

USAGE
    mup <command> [options]

COMMANDS
    mup <file>              Convert file to HTML
    mup <file>.md           Convert Markdown to HTML
    mup new <name>          Create a new .mup file
    mup open <file>         View file in terminal
    mup check <file>        Validate file for errors
    mup init [name]         Create a new project

OPTIONS
    -d, --dark              Use dark theme
    -l, --light             Use light theme (default)
    -r, --rtl               Right-to-left layout
        --ltr               Left-to-right layout
    -o, --output <file>     Output file path
        --css <file>        Apply custom CSS file
        --debug             Show debug info
    -h, --help              Show this help
    -v, --version           Show version

EXAMPLES
    mup hello.mup                    Convert hello.mup
    mup readme.md                    Convert markdown to HTML
    mup hello.mup --dark             Dark theme
    mup hello.mup --css theme.css    Custom CSS theme
    mup hello.mup --debug            Show debug info
    mup new my-doc                   Create my-doc.mup
    mup open hello.mup               View in terminal
    mup check hello.mup              Validate file
"""


def main() -> int:
    """Main CLI entry point."""
    args = sys.argv[1:]

    # No arguments — show help
    if not args:
        print(HELP_TEXT)
        return 0

    # Parse global flags
    show_help = False
    show_version = False
    dark = False
    light = False
    rtl = False
    ltr = False
    show_debug = False
    output = None
    css_file = None

    remaining = []
    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ("-h", "--help"):
            show_help = True
        elif arg in ("-v", "--version"):
            show_version = True
        elif arg in ("-d", "--dark"):
            dark = True
        elif arg in ("-l", "--light"):
            light = True
        elif arg in ("-r", "--rtl"):
            rtl = True
        elif arg == "--ltr":
            ltr = True
        elif arg == "--debug":
            show_debug = True
        elif arg == "--css":
            if i + 1 < len(args):
                css_file = args[i + 1]
                i += 1
            else:
                print(theme.error("Error: --css requires a file path"))
                return 1
        elif arg in ("-o", "--output"):
            if i + 1 < len(args):
                output = args[i + 1]
                i += 1
            else:
                print(theme.error("Error: --output requires a value"))
                return 1
        else:
            remaining.append(arg)

        i += 1

    # Handle --help / --version
    if show_help:
        print(HELP_TEXT)
        return 0

    if show_version:
        print(f"Markup+ v{__version__}")
        return 0

    # Determine theme
    theme_name = "dark" if dark else "light"

    # Determine direction
    direction = None
    if rtl:
        direction = "rtl"
    elif ltr:
        direction = "ltr"

    # No command
    if not remaining:
        print(HELP_TEXT)
        return 0

    # Dispatch commands
    command = remaining[0]
    command_args = remaining[1:]

    from . import commands

    if command == "new":
        if not command_args:
            print(theme.error("Error: 'new' requires a name"))
            print(theme.dim("Usage: mup new <name>"))
            return 1
        return commands.new_file(command_args[0])

    if command == "open":
        if not command_args:
            print(theme.error("Error: 'open' requires a file"))
            print(theme.dim("Usage: mup open <file>"))
            return 1
        return commands.open_file(command_args[0])

    if command == "check":
        if not command_args:
            print(theme.error("Error: 'check' requires a file"))
            print(theme.dim("Usage: mup check <file>"))
            return 1
        return commands.check_file(command_args[0])
    if command == "init":
        name = command_args[0] if command_args else None
        return commands.init_project(name)

    # Default: treat as file path
    return commands.build_file(
        command,
        theme_name=theme_name,
        direction=direction,
        output=output,
        show_debug=show_debug,
        css_file=css_file,
    )
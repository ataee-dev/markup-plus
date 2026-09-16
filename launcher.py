"""
PyInstaller entry point for Markup+.

This file is used by PyInstaller to create a standalone executable.
It imports the CLI main function and runs it.
"""

import sys


def main() -> int:
    """Entry point for the standalone executable."""
    try:
        from markup_plus.cli import main as cli_main
        return cli_main()
    except ImportError as e:
        print(f"Error: Could not import markup_plus. {e}", file=sys.stderr)
        print("This may indicate a corrupted installation.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
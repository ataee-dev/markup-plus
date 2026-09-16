"""
CLI Commands — Implementation of all `mup` subcommands.
"""

import re
import sys
import time
from pathlib import Path
from typing import Optional

from . import theme
from .errors import (
    show_error, show_success, show_info, show_warning,
    show_source_context, show_debug_info, show_stats,
)
from .display import view_file


# ============================================================
# Convert command (main)
# ============================================================

def build_file(
    path_str: str,
    theme_name: str = "light",
    direction: Optional[str] = None,
    output: Optional[str] = None,
    show_debug: bool = False,
    css_file: Optional[str] = None,
) -> int:
    """Convert a .mup file (or .md) to HTML."""
    from ..renderer import to_html
    from ..parser import parse_text

    input_file = Path(path_str)

    # ---- Check file exists ----
    if not input_file.exists():
        show_error(f"File not found: {input_file}")
        return 1

    # ---- Check CSS file (if provided) ----
    if css_file:
        css_path = Path(css_file)
        if not css_path.exists():
            show_error(f"CSS file not found: {css_file}")
            return 1
        if not css_path.is_file():
            show_error(f"CSS path is not a file: {css_file}")
            return 1
        # Resolve to absolute path so it works from any CWD
        css_file = str(css_path.resolve())

    # ---- Read input ----
    try:
        text = input_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        show_error(f"File is not valid UTF-8: {input_file}")
        return 1
    except Exception as e:
        show_error(f"Could not read file: {e}")
        return 1

    # ---- Convert ----
    start_time = time.time()

    try:
        html = to_html(
            text,
            title=input_file.stem,
            theme=theme_name,
            direction=direction,
            base_dir=str(input_file.parent),
            custom_css=css_file,
        )
    except Exception as e:
        show_error(f"Conversion failed: {e}")

        # Try to find error line
        if hasattr(e, "line") and e.line > 0:
            show_source_context(input_file, e.line)

        if show_debug:
            import traceback
            traceback.print_exc()

        return 1

    elapsed = (time.time() - start_time) * 1000  # ms

    # ---- Determine output path ----
    if output:
        output_file = Path(output)
    else:
        output_file = input_file.with_suffix(".html")

    # ---- Write output ----
    try:
        output_file.write_text(html, encoding="utf-8")
    except Exception as e:
        show_error(f"Could not write output: {e}")
        return 1

    # ---- Report ----
    show_success(f"{input_file} → {output_file}")

    if css_file:
        show_info(f"Custom CSS: {css_file}")

    # ---- Debug info ----
    if show_debug:
        doc = parse_text(text)

        # Count different node types
        node_types = {}
        for child in doc.children:
            name = type(child).__name__
            node_types[name] = node_types.get(name, 0) + 1

        show_debug_info({
            "Input": str(input_file),
            "Output": str(output_file),
            "Theme": theme_name,
            "Custom CSS": css_file or "(none)",
            "Direction": direction or "auto",
            "Lines": len(text.split("\n")),
            "Input size": f"{len(text):,} chars",
            "Output size": f"{len(html):,} chars",
            "Elapsed": f"{elapsed:.1f} ms",
            "Variables": len(doc.variables),
            "Footnotes": len(doc.footnotes),
        })

        show_stats(node_types)

    return 0


# ============================================================
# New file command
# ============================================================

TEMPLATE_NEW = """# {title}

Welcome to **Markup+**!

## Features

- **Bold** and *italic*
- `Inline code`

@note
This is a note.
@end

## Next Steps

Start writing your document here...
"""


def new_file(name: str, template: str = "default") -> int:
    """Create a new .mup file with a template."""
    # Ensure .mup extension
    if not name.endswith(".mup"):
        name += ".mup"

    path = Path(name)

    if path.exists():
        show_error(f"File already exists: {path}")
        return 1

    # Build content
    content = TEMPLATE_NEW.format(title=path.stem)

    # Write
    try:
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        show_error(f"Could not create file: {e}")
        return 1

    show_success(f"Created: {path}")
    show_info(f"Open with: mup open {path}")
    return 0


# ============================================================
# View file in terminal
# ============================================================

def open_file(path_str: str, show_numbers: bool = True) -> int:
    """Display a .mup file in the terminal."""
    path = Path(path_str)

    if not path.exists():
        show_error(f"File not found: {path}")
        return 1

    view_file(path, show_numbers=show_numbers)
    return 0


# ============================================================
# Check / validate file
# ============================================================

def check_file(path_str: str) -> int:
    """Check a .mup file for errors and warnings."""
    from ..parser import parse_text

    path = Path(path_str)

    if not path.exists():
        show_error(f"File not found: {path}")
        return 1

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        show_error(f"File is not valid UTF-8: {path}")
        return 1

    print()
    print(theme.header(f"🔍 Checking: {path.name}"))
    print(theme.dim("─" * 50))
    print()

    # Count blocks
    warnings = []
    errors = []
    doc = None
    blocks_count = 0

    try:
        doc = parse_text(text)
        blocks_count = len(doc.children)

        # Check for empty document
        if blocks_count == 0:
            warnings.append("Document is empty")

        # Check for undefined variables
        used_vars = set(re.findall(r"\{([a-zA-Z_]\w*)\}", text))
        defined_vars = set(doc.variables.keys())
        undefined = used_vars - defined_vars

        if undefined:
            warnings.append(
                f"Undefined variables: {', '.join(sorted(undefined))}"
            )

        # Check for unbalanced directives
        open_blocks = len(re.findall(
            r"^@(if|each|tabs|collapse|def|note|warning|tip|danger|success|quote|timeline|gallery)\b",
            text,
            re.MULTILINE,
        ))
        close_blocks = len(re.findall(r"^@end\b", text, re.MULTILINE))

        if open_blocks != close_blocks:
            warnings.append(
                f"Unbalanced blocks: {open_blocks} opened, {close_blocks} closed"
            )

    except Exception as e:
        errors.append(str(e))

    # Report
    if errors:
        for err in errors:
            show_error(err)
        print()
        return 1

    if warnings:
        for w in warnings:
            show_warning(w)
        print()

    # Summary
    show_info(f"Blocks: {blocks_count}")
    show_info(f"Lines: {len(text.split(chr(10)))}")
    if doc:
        show_info(f"Variables: {len(doc.variables)}")
        show_info(f"Footnotes: {len(doc.footnotes)}")

    print()

    if not errors and not warnings:
        show_success("No issues found!")

    print()
    return 0 if not errors else 1


# ============================================================
# Init project
# ============================================================

def init_project(name: Optional[str] = None) -> int:
    """Create a new Markup+ project."""
    project_dir = Path(name) if name else Path.cwd()

    if not project_dir.exists():
        project_dir.mkdir(parents=True)

    # Create structure
    (project_dir / "docs").mkdir(exist_ok=True)
    (project_dir / "assets").mkdir(exist_ok=True)

    # Create index.mup
    index = project_dir / "index.mup"
    if not index.exists():
        index.write_text(
            f"# {project_dir.name}\n\nWelcome to my project!\n",
            encoding="utf-8",
        )

    show_success(f"Project initialized: {project_dir}")
    show_info(f"Created: {index}")
    return 0
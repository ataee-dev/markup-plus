"""
Markup+ Parser

Converts tokens into an Abstract Syntax Tree (AST).

Phase 1:  Headings, Paragraphs
Phase 2:  Lists, Blockquotes, HR, Code blocks, Images, Galleries
Phase 3:  Links, Tables, Task Lists, Front Matter, TOC, Footnotes
"""

import re
from typing import List

from .ast import (
    BlockQuote,
    CodeBlock,
    Document,
    GalleryBlock,
    Heading,
    HorizontalRule,
    ImageBlock,
    ListBlock,
    Paragraph,
    TableBlock,
    TOCBlock,
)
from .lexer import Lexer, Token


# ============================================================
# Regex patterns
# ============================================================

RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_UL_ITEM = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
RE_TASK_ITEM = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(.+?)\s*$")
RE_OL_ITEM = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")
RE_HR = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
RE_BLOCKQUOTE = re.compile(r"^\s*>\s?(.*)$")
RE_CODE_FENCE = re.compile(r"^\s*```\s*(\w*)\s*(?:\{(.+?)\})?\s*$")
RE_IMAGE = re.compile(
    r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'
    r'(?:\{([^}]*)\})?\s*$'
)
RE_GALLERY_START = re.compile(r"^@gallery(?:\s*\{([^}]*)\})?\s*$")
RE_GALLERY_END = re.compile(r"^@end\s*$")
RE_TABLE_LINE = re.compile(r"^\s*\|.*\|\s*$")
RE_TABLE_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
RE_FRONT_MATTER_START = re.compile(r"^---\s*$")
RE_FRONT_MATTER_KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.+?)\s*$")
RE_TOC = re.compile(r"^@toc(?:\s*\{([^}]*)\})?\s*$")
RE_FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:\s*(.+?)\s*$")


class Parser:
    """Parse a list of tokens into a Document AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    # --------------------------------------------------------
    # Main parse loop
    # --------------------------------------------------------

    def parse(self) -> Document:
        doc = Document()

        # 1. Parse front matter (must be first)
        self._parse_front_matter(doc)

        # 2. First pass: collect footnote definitions
        self._collect_footnotes(doc)

        # 3. Reset position and parse main content
        self.pos = doc._content_start if hasattr(doc, "_content_start") else 0
        self._parse_content(doc)

        # 4. Assign slugs to headings (for TOC)
        self._assign_heading_slugs(doc)

        return doc

    def _parse_content(self, doc: Document) -> None:
        """Parse main content into blocks."""
        while not self._is_at_end():
            token = self._peek()

            if token.type == "EOF":
                self._advance()
                continue

            line = token.value

            # Skip blank lines
            if line.strip() == "":
                self._advance()
                continue

            # Footnote definition (skip — already collected)
            if RE_FOOTNOTE_DEF.match(line.strip()):
                self._advance()
                continue

            # Code fence: ```lang {options}
            m = RE_CODE_FENCE.match(line)
            if m:
                doc.children.append(
                    self._parse_code_block(m.group(1), m.group(2), token.line)
                )
                continue

            # Gallery: @gallery {options} ... @end
            m = RE_GALLERY_START.match(line.strip())
            if m:
                doc.children.append(self._parse_gallery(m.group(1), token.line))
                continue

            # TOC: @toc {title="..."}
            m = RE_TOC.match(line.strip())
            if m:
                options_str = m.group(1) or ""
                options = self._parse_gallery_options(options_str)
                toc_title = options.get("title", "")
                doc.children.append(TOCBlock(title=toc_title, line=token.line))
                self._advance()
                continue

            # Table
            if self._is_table_start():
                doc.children.append(self._parse_table())
                continue

            # Image
            m = RE_IMAGE.match(line.strip())
            if m:
                doc.children.append(self._parse_image(m, token.line))
                self._advance()
                continue

            # Horizontal rule
            if RE_HR.match(line):
                doc.children.append(HorizontalRule(line=token.line))
                self._advance()
                continue

            # Heading
            m = RE_HEADING.match(line)
            if m:
                doc.children.append(
                    Heading(
                        level=len(m.group(1)),
                        text=m.group(2),
                        line=token.line,
                    )
                )
                self._advance()
                continue

            # Blockquote
            if RE_BLOCKQUOTE.match(line):
                doc.children.append(self._parse_blockquote())
                continue

            # Task list
            if RE_TASK_ITEM.match(line):
                doc.children.append(self._parse_task_list())
                continue

            # Unordered list
            if RE_UL_ITEM.match(line):
                doc.children.append(self._parse_ul())
                continue

            # Ordered list
            if RE_OL_ITEM.match(line):
                doc.children.append(self._parse_ol())
                continue

            # Paragraph
            doc.children.append(Paragraph(text=line, line=token.line))
            self._advance()

    # --------------------------------------------------------
    # Front matter
    # --------------------------------------------------------

    def _parse_front_matter(self, doc: Document) -> None:
        """Parse YAML-like front matter at the top of the document."""
        if self._is_at_end():
            doc._content_start = 0
            return

        first = self._peek().value
        if not RE_FRONT_MATTER_START.match(first):
            doc._content_start = 0
            return

        saved_pos = self.pos
        self._advance()  # consume opening ---

        meta = {}
        found_closing = False

        while not self._is_at_end():
            line = self._peek().value

            if RE_FRONT_MATTER_START.match(line):
                self._advance()
                found_closing = True
                break

            if line.strip() == "":
                self._advance()
                continue

            m = RE_FRONT_MATTER_KEY.match(line)
            if m:
                key = m.group(1)
                value = m.group(2).strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                meta[key] = value
                self._advance()
            else:
                self.pos = saved_pos
                doc._content_start = 0
                return

        if not found_closing:
            self.pos = saved_pos
            doc._content_start = 0
            return

        doc.meta = meta
        doc._content_start = self.pos

    # --------------------------------------------------------
    # Footnotes
    # --------------------------------------------------------

    def _collect_footnotes(self, doc: Document) -> None:
        """Collect all footnote definitions from the document."""
        for token in self.tokens:
            line = token.value.strip()
            m = RE_FOOTNOTE_DEF.match(line)
            if m:
                key = m.group(1)
                text = m.group(2)
                doc.footnotes[key] = text

    # --------------------------------------------------------
    # Heading slugs (for TOC)
    # --------------------------------------------------------

    def _assign_heading_slugs(self, doc: Document) -> None:
        """Generate slugs for all headings (used by TOC)."""
        seen = {}
        for child in doc.children:
            if isinstance(child, Heading):
                slug = self._slugify(child.text)
                if slug in seen:
                    seen[slug] += 1
                    slug = f"{slug}-{seen[slug]}"
                else:
                    seen[slug] = 0
                child.slug = slug

    @staticmethod
    def _slugify(text: str) -> str:
        """Create a URL-friendly slug from text."""
        text = text.lower().strip()
        # Keep alphanumerics, Persian/Arabic letters, and dashes
        text = re.sub(r"[^\w\u0600-\u06FF\u0750-\u077F\s-]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        text = re.sub(r"-+", "-", text)
        return text.strip("-") or "section"

    # --------------------------------------------------------
    # Table parser
    # --------------------------------------------------------

    def _is_table_start(self) -> bool:
        if self._is_at_end():
            return False

        line1 = self._peek().value
        if not RE_TABLE_LINE.match(line1):
            return False

        if self.pos + 1 >= len(self.tokens):
            return False

        line2 = self.tokens[self.pos + 1].value
        if not RE_TABLE_SEP.match(line2):
            return False

        if "-" not in line2:
            return False

        return True

    def _parse_table(self) -> TableBlock:
        start_line = self._peek().line

        header_line = self._peek().value
        headers = self._split_table_row(header_line)
        self._advance()

        sep_line = self._peek().value
        alignments = self._parse_alignments(sep_line)
        self._advance()

        while len(alignments) < len(headers):
            alignments.append("none")
        alignments = alignments[:len(headers)]

        rows: List[List[str]] = []
        while not self._is_at_end():
            line = self._peek().value
            if not RE_TABLE_LINE.match(line):
                break
            if RE_TABLE_SEP.match(line):
                self._advance()
                continue
            cells = self._split_table_row(line)
            while len(cells) < len(headers):
                cells.append("")
            cells = cells[:len(headers)]
            rows.append(cells)
            self._advance()

        return TableBlock(
            headers=headers,
            rows=rows,
            alignments=alignments,
            line=start_line,
        )

    def _split_table_row(self, line: str) -> List[str]:
        line = line.strip()
        if line.startswith("|"):
            line = line[1:]
        if line.endswith("|"):
            line = line[:-1]
        return [cell.strip() for cell in line.split("|")]

    def _parse_alignments(self, line: str) -> List[str]:
        cells = self._split_table_row(line)
        alignments = []
        for cell in cells:
            cell = cell.strip()
            left = cell.startswith(":")
            right = cell.endswith(":")
            if left and right:
                alignments.append("center")
            elif right:
                alignments.append("right")
            elif left:
                alignments.append("left")
            else:
                alignments.append("none")
        return alignments

    # --------------------------------------------------------
    # Gallery parser
    # --------------------------------------------------------

    def _parse_gallery(self, options_str: str, start_line: int) -> GalleryBlock:
        self._advance()

        options = self._parse_gallery_options(options_str or "")

        try:
            columns = int(options.get("columns", 3))
        except (ValueError, TypeError):
            columns = 3

        columns = max(1, min(columns, 6))
        caption = options.get("caption", "")

        images: List[ImageBlock] = []

        while not self._is_at_end():
            line = self._peek().value.strip()

            if RE_GALLERY_END.match(line):
                self._advance()
                break

            if line == "":
                self._advance()
                continue

            m = RE_IMAGE.match(line)
            if m:
                images.append(self._parse_image(m, self._peek().line))
                self._advance()
                continue

            self._advance()

        return GalleryBlock(
            columns=columns,
            images=images,
            caption=caption,
            line=start_line,
        )

    def _parse_gallery_options(self, options_str: str) -> dict:
        if not options_str:
            return {}
        options = {}
        pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|(\S+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            if value:
                options[key] = value
            else:
                options[key] = True
        return options

    # --------------------------------------------------------
    # Image parser
    # --------------------------------------------------------

    def _parse_image(self, match: re.Match, line_num: int) -> ImageBlock:
        alt = match.group(1)
        url = match.group(2)
        title = match.group(3) or ""
        options_str = match.group(4) or ""

        options = self._parse_image_options(options_str)

        zoomable = options.get("zoomable", True)
        if isinstance(zoomable, str):
            zoomable = zoomable.lower() != "false"

        return ImageBlock(
            alt=alt,
            url=url,
            title=title,
            width=options.get("width", ""),
            height=options.get("height", ""),
            align=options.get("align", ""),
            link=options.get("link", ""),
            caption=options.get("caption", ""),
            description=options.get("desc", ""),
            zoomable=zoomable,
            line=line_num,
        )

    def _parse_image_options(self, options_str: str) -> dict:
        if not options_str:
            return {}
        options = {}
        pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|(\S+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            if value:
                options[key] = value
            else:
                options[key] = True
        return options

    # --------------------------------------------------------
    # Code block parser
    # --------------------------------------------------------

    def _parse_code_block(
        self, language: str, options_str: str, start_line: int
    ) -> CodeBlock:
        self._advance()
        code_lines: List[str] = []

        while not self._is_at_end():
            line = self._peek().value
            if RE_CODE_FENCE.match(line):
                self._advance()
                break
            code_lines.append(line)
            self._advance()

        options = self._parse_code_options(options_str or "")

        return CodeBlock(
            language=language,
            code="\n".join(code_lines),
            title=options.get("title", ""),
            copy=options.get("copy", True),
            download=options.get("download", True),
            run=options.get("run", False),
            share=options.get("share", False),
            linenos=options.get("linenos", False),
            highlight=options.get("hl", []),
            wrap=options.get("wrap", False),
            line=start_line,
        )

    def _parse_code_options(self, options_str: str) -> dict:
        if not options_str:
            return {}
        options = {}
        pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|\[([^\]]*)\]|(\w+)))?')
        for match in pattern.finditer(options_str):
            key = match.group(1)
            str_val = match.group(2)
            list_val = match.group(3)
            word_val = match.group(4)

            if str_val is not None:
                options[key] = str_val
            elif list_val is not None:
                options[key] = [
                    int(x.strip()) for x in list_val.split(",") if x.strip()
                ]
            elif word_val is not None:
                if word_val == "true":
                    options[key] = True
                elif word_val == "false":
                    options[key] = False
                else:
                    options[key] = word_val
            else:
                options[key] = True
        return options

    # --------------------------------------------------------
    # Blockquote / List / TaskList parsers
    # --------------------------------------------------------

    def _parse_blockquote(self) -> BlockQuote:
        start_line = self._peek().line
        lines: List[str] = []

        while not self._is_at_end():
            line = self._peek().value
            m = RE_BLOCKQUOTE.match(line)
            if not m:
                break
            lines.append(m.group(1))
            self._advance()

        return BlockQuote(text="\n".join(lines), line=start_line)

    def _parse_task_list(self) -> ListBlock:
        start_line = self._peek().line
        items: List[str] = []
        checked: List[bool] = []

        while not self._is_at_end():
            line = self._peek().value
            m = RE_TASK_ITEM.match(line)
            if not m:
                break
            checkbox = m.group(1)
            text = m.group(2)
            items.append(text)
            checked.append(checkbox.lower() == "x")
            self._advance()

        return ListBlock(
            ordered=False,
            items=items,
            checked=checked,
            line=start_line,
        )

    def _parse_ul(self) -> ListBlock:
        start_line = self._peek().line
        items: List[str] = []

        while not self._is_at_end():
            line = self._peek().value
            m = RE_UL_ITEM.match(line)
            if not m:
                break
            items.append(m.group(1))
            self._advance()

        return ListBlock(ordered=False, items=items, line=start_line)

    def _parse_ol(self) -> ListBlock:
        start_line = self._peek().line
        items: List[str] = []

        while not self._is_at_end():
            line = self._peek().value
            m = RE_OL_ITEM.match(line)
            if not m:
                break
            items.append(m.group(1))
            self._advance()

        return ListBlock(ordered=True, items=items, line=start_line)

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if not self._is_at_end():
            self.pos += 1
        return token

    def _is_at_end(self) -> bool:
        return self.tokens[self.pos].type == "EOF"


def parse_text(text: str) -> Document:
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
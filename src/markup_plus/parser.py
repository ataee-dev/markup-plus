"""
Markup+ Parser

Converts tokens into an Abstract Syntax Tree (AST).

Phase 1:  Headings, Paragraphs
Phase 2:  Lists, Blockquotes, HR, Code blocks, Images
"""

import re
from typing import List

from .ast import (
    BlockQuote,
    CodeBlock,
    Document,
    Heading,
    HorizontalRule,
    ImageBlock,
    ListBlock,
    Paragraph,
)
from .lexer import Lexer, Token


# Regex patterns
RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_UL_ITEM = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
RE_OL_ITEM = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")
RE_HR = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
RE_BLOCKQUOTE = re.compile(r"^\s*>\s?(.*)$")
RE_CODE_FENCE = re.compile(r"^\s*```\s*(\w*)\s*(?:\{(.+?)\})?\s*$")
# Image: ![alt](url "title"){options}
RE_IMAGE = re.compile(
    r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)'
    r'(?:\{([^}]*)\})?\s*$'
)


class Parser:
    """Parse a list of tokens into a Document AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Document:
        doc = Document()

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

            # Code fence: ```lang {options}
            m = RE_CODE_FENCE.match(line)
            if m:
                doc.children.append(
                    self._parse_code_block(m.group(1), m.group(2), token.line)
                )
                continue

            # Image: ![alt](url) — must come before paragraph
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

        return doc

    # --------------------------------------------------------
    # Image parser
    # --------------------------------------------------------

    def _parse_image(self, match: re.Match, line_num: int) -> ImageBlock:
        alt = match.group(1)
        url = match.group(2)
        title = match.group(3) or ""
        options_str = match.group(4) or ""

        options = self._parse_image_options(options_str)

        return ImageBlock(
            alt=alt,
            url=url,
            title=title,
            width=options.get("width", ""),
            height=options.get("height", ""),
            align=options.get("align", ""),
            link=options.get("link", ""),
            caption=options.get("caption", ""),
            line=line_num,
        )

    def _parse_image_options(self, options_str: str) -> dict:
        """Parse 'width=400 align=center' into a dict."""
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
    # Block parsers
    # --------------------------------------------------------

    def _parse_code_block(
        self, language: str, options_str: str, start_line: int
    ) -> CodeBlock:
        """Parse ```lang {options} ... ``` fenced block."""
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
"""
Markup+ Parser

Converts tokens into an Abstract Syntax Tree (AST).

Phase 1:  Headings, Paragraphs
Phase 2:  Lists, Blockquotes, Horizontal rules
"""

import re
from typing import List

from .ast import (
    BlockQuote,
    Document,
    Heading,
    HorizontalRule,
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

            # Horizontal rule (must be before UL, since --- is also a valid UL marker)
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
    # Block parsers
    # --------------------------------------------------------

    def _parse_blockquote(self) -> BlockQuote:
        """Parse consecutive > lines."""
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
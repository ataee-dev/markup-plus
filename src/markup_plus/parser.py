"""
Markup+ Parser (Phase 1)

Converts tokens into an Abstract Syntax Tree (AST).

Phase 1 supports:
    - Headings (H1, H2, H3)
    - Paragraphs
    - Empty lines (skipped)
"""

import re
from typing import List

from .ast import Document, Heading, Paragraph
from .lexer import Lexer, Token


# Regex patterns for block-level constructs
RE_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


class Parser:
    """Parse a list of tokens into a Document AST."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> Document:
        """Parse tokens into a Document node."""
        doc = Document()

        while not self._is_at_end():
            token = self._peek()

            # Skip EOF
            if token.type == "EOF":
                self._advance()
                continue

            line = token.value

            # Skip blank lines
            if line.strip() == "":
                self._advance()
                continue

            # Heading: # Title / ## Title / ### Title
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

            # Paragraph (everything else)
            doc.children.append(Paragraph(text=line, line=token.line))
            self._advance()

        return doc

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
    """Convenience function: source text -> Document AST."""
    lexer = Lexer(text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()
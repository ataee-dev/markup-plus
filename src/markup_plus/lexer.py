"""
Markup+ Lexer

Splits source text into tokens. Markup+ uses a line-based
approach since most constructs are line-oriented.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    """A single token from source text."""
    type: str
    value: str
    line: int


class Lexer:
    """Tokenize Markup+ source code into a flat list of tokens."""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split("\n")

    def tokenize(self) -> List[Token]:
        """Return list of tokens, one per line, plus EOF."""
        tokens: List[Token] = []

        for i, line in enumerate(self.lines, start=1):
            tokens.append(Token(type="LINE", value=line, line=i))

        tokens.append(Token(type="EOF", value="", line=len(self.lines) + 1))
        return tokens
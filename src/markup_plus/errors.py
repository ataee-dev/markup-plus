"""
Markup+ Error Classes

Defines custom exceptions used across the Markup+ library.
"""


class MarkupError(Exception):
    """Base exception for all Markup+ errors."""

    def __init__(self, message: str, line: int = 0, column: int = 0):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self._format())

    def _format(self) -> str:
        if self.line > 0:
            return f"[Line {self.line}] {self.message}"
        return self.message


class LexerError(MarkupError):
    """Raised when the lexer encounters invalid input."""
    pass


class ParserError(MarkupError):
    """Raised when the parser encounters invalid syntax."""
    pass


class RenderError(MarkupError):
    """Raised when the renderer fails."""
    pass


class EvaluationError(MarkupError):
    """Raised when variable/expression evaluation fails."""
    pass
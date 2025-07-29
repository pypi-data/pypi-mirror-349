"""Lexer for SQLFlow DSL."""

import json
import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Pattern, Tuple

# Regex patterns for JSON parsing
WHITESPACE = re.compile(r"[ \t\n\r]+")
JSON_STRING = re.compile(r'"(?:\\.|[^"\\])*"')
VARIABLE_PATTERN = re.compile(r"\${[^}]+}")


def replace_variables_for_validation(
    text: str, dummy_values: Dict[str, Any] = None
) -> str:
    """Replace ${var} style variables with dummy values for JSON validation."""
    if dummy_values is None:
        dummy_values = {"run_date": "2023-01-01"}

    def replace_var(match):
        var = match.group(0)[2:-1]  # Strip ${ and }
        if "|" in var:
            var = var.split("|")[0]
        return f'"{dummy_values.get(var, "dummy")}"'

    # First, replace variables with dummy values
    text_with_vars_replaced = VARIABLE_PATTERN.sub(replace_var, text)

    # Remove trailing commas in JSON objects and arrays which are invalid in standard JSON
    # but common in code - handle both objects/arrays and multi-line formats
    text_with_fixed_commas = re.sub(r",(\s*[}\]])", r"\1", text_with_vars_replaced)

    return text_with_fixed_commas


class TokenType(Enum):
    """Token types for SQLFlow DSL."""

    SOURCE = auto()
    TYPE = auto()
    PARAMS = auto()
    LOAD = auto()
    FROM = auto()
    EXPORT = auto()
    TO = auto()
    OPTIONS = auto()
    SELECT = auto()
    INCLUDE = auto()
    AS = auto()
    SET = auto()
    CREATE = auto()
    TABLE = auto()

    # Conditional execution tokens
    IF = auto()
    THEN = auto()
    ELSE_IF = auto()  # Matches "ELSEIF" or "ELSE IF"
    ELSE = auto()
    END_IF = auto()  # Matches "ENDIF" or "END IF"

    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    JSON_OBJECT = auto()
    VARIABLE = auto()  # For ${var} style variables
    VARIABLE_DEFAULT = auto()  # For default values in ${var|default}

    SEMICOLON = auto()
    EQUALS = auto()  # For assignment operations
    PIPE = auto()  # For variable default values
    DOLLAR = auto()  # For variable references
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    DOT = (
        auto()
    )  # For SQL table.column references - IMPORTANT: Prevents spaces between identifiers and dots

    SQL_BLOCK = auto()

    WHITESPACE = auto()
    COMMENT = auto()
    ERROR = auto()
    EOF = auto()


@dataclass
class Token:
    """Token in the SQLFlow DSL."""

    type: TokenType
    value: str
    line: int = 1
    column: int = 1


class Lexer:
    """Lexer for SQLFlow DSL.

    The lexer tokenizes the input text into a sequence of tokens.
    """

    def __init__(self, text: str):
        """Initialize the lexer with input text.

        Args:
            text: The input text to tokenize
        """
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

        self.patterns: List[Tuple[TokenType, Pattern]] = [
            (TokenType.WHITESPACE, re.compile(r"\s+")),
            (TokenType.COMMENT, re.compile(r"--.*?(?:\n|$)")),
            (TokenType.SOURCE, re.compile(r"SOURCE\b", re.IGNORECASE)),
            (TokenType.TYPE, re.compile(r"TYPE\b", re.IGNORECASE)),
            (TokenType.PARAMS, re.compile(r"PARAMS\b", re.IGNORECASE)),
            (TokenType.LOAD, re.compile(r"LOAD\b", re.IGNORECASE)),
            (TokenType.FROM, re.compile(r"FROM\b", re.IGNORECASE)),
            (TokenType.EXPORT, re.compile(r"EXPORT\b", re.IGNORECASE)),
            (TokenType.TO, re.compile(r"TO\b", re.IGNORECASE)),
            (TokenType.OPTIONS, re.compile(r"OPTIONS\b", re.IGNORECASE)),
            (TokenType.SELECT, re.compile(r"SELECT\b", re.IGNORECASE)),
            (TokenType.INCLUDE, re.compile(r"INCLUDE\b", re.IGNORECASE)),
            (TokenType.AS, re.compile(r"AS\b", re.IGNORECASE)),
            (TokenType.SET, re.compile(r"SET\b", re.IGNORECASE)),
            (TokenType.CREATE, re.compile(r"CREATE\b", re.IGNORECASE)),
            (TokenType.TABLE, re.compile(r"TABLE\b", re.IGNORECASE)),
            # Conditional execution patterns
            (TokenType.IF, re.compile(r"IF\b", re.IGNORECASE)),
            (TokenType.THEN, re.compile(r"THEN\b", re.IGNORECASE)),
            (TokenType.ELSE_IF, re.compile(r"ELSE\s*IF\b", re.IGNORECASE)),
            (TokenType.ELSE, re.compile(r"ELSE\b", re.IGNORECASE)),
            (TokenType.END_IF, re.compile(r"END\s*IF\b", re.IGNORECASE)),
            (TokenType.EQUALS, re.compile(r"=")),
            (TokenType.PIPE, re.compile(r"\|")),
            (TokenType.DOLLAR, re.compile(r"\$")),
            (TokenType.LEFT_BRACE, re.compile(r"{")),
            (TokenType.RIGHT_BRACE, re.compile(r"}")),
            (TokenType.SEMICOLON, re.compile(r";")),
            (TokenType.DOT, re.compile(r"\.")),  # SQL dot operator for table.column
            # Handle ${var} or ${var|default} style variables
            (TokenType.VARIABLE, re.compile(r"\$\{[^}]+\}")),
            (
                TokenType.STRING,
                re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\''),
            ),  # Handle both " and ' quotes
            (TokenType.NUMBER, re.compile(r"\d+(?:\.\d+)?")),
            (TokenType.IDENTIFIER, re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")),
        ]

    def tokenize(self) -> List[Token]:
        """Tokenize the input text.

        Returns:
            List of tokens
        """
        while self.pos < len(self.text):
            self._tokenize_next()

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _tokenize_next(self) -> None:
        """Tokenize the next token in the input text."""
        # Check for JSON object first
        if self.text[self.pos] == "{":
            json_value, success = self._extract_json_object()
            if success:
                self.tokens.append(
                    Token(TokenType.JSON_OBJECT, json_value, self.line, self.column)
                )
                for char in json_value:
                    if char == "\n":
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1
                self.pos += len(json_value)
                return

        for token_type, pattern in self.patterns:
            match = pattern.match(self.text[self.pos :])
            if match:
                value = match.group(0)

                if token_type not in (TokenType.WHITESPACE, TokenType.COMMENT):
                    self.tokens.append(Token(token_type, value, self.line, self.column))

                for char in value:
                    if char == "\n":
                        self.line += 1
                        self.column = 1
                    else:
                        self.column += 1

                self.pos += len(value)
                return

        self.tokens.append(
            Token(TokenType.ERROR, self.text[self.pos], self.line, self.column)
        )
        self.column += 1
        self.pos += 1

    def _is_character_in_string(
        self, in_string: bool, escape_next: bool, char: str
    ) -> Tuple[bool, bool]:
        """Determine if we're inside a string and handle escape sequences.

        Args:
            in_string: Whether we're currently inside a string
            escape_next: Whether the next character should be escaped
            char: The current character

        Returns:
            Tuple of (new in_string status, new escape_next status)
        """
        if escape_next:
            return in_string, False

        if char == "\\" and in_string:
            return in_string, True

        if char == '"' and not escape_next:
            return not in_string, False

        return in_string, False

    def _update_json_depth(self, char: str, in_string: bool, depth: int) -> int:
        """Update JSON nesting depth based on braces when not in a string.

        Args:
            char: Current character
            in_string: Whether we're inside a string
            depth: Current depth

        Returns:
            New depth value
        """
        if in_string:
            return depth

        if char == "{":
            return depth + 1
        elif char == "}":
            return depth - 1

        return depth

    def _check_json_validity(self, json_text: str) -> bool:
        """Check if the JSON is valid, with variable replacement handling.

        Args:
            json_text: JSON text to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            # Replace variables for validation
            json_text_for_validation = replace_variables_for_validation(json_text)
            # Strict checking of the exact JSON as written, keeping formatting
            json.loads(json_text_for_validation)
            return True
        except json.JSONDecodeError:
            return False

    def _extract_json_object(self) -> Tuple[str, bool]:
        """Extract a JSON object from the input text.

        Handles both single-line and multi-line JSON objects, preserving formatting.
        Properly handles nested objects, arrays, and quoted strings.

        Returns:
            Tuple of (json_text, success)
        """
        if self.text[self.pos] != "{":
            return "", False

        depth = 0
        in_string = False
        escape_next = False
        start_pos = self.pos
        start_line = self.line
        start_col = self.column

        current_line = self.line
        current_col = self.column

        i = start_pos
        while i < len(self.text):
            char = self.text[i]

            # Track string state and handle escape sequences
            in_string, escape_next = self._is_character_in_string(
                in_string, escape_next, char
            )

            # Track JSON structure depth
            depth = self._update_json_depth(char, in_string, depth)

            # Check if we've reached the end of the JSON object
            if not in_string and char == "}" and depth == 0:
                # Found the end of the JSON object
                json_text = self.text[start_pos : i + 1]

                # Validate JSON structure
                if self._check_json_validity(json_text):
                    self.line = current_line
                    self.column = current_col + 1
                    return json_text, True
                else:
                    # Keep searching if invalid to find potential multi-line JSON
                    depth = 1

            # Track line numbers
            if char == "\n":
                current_line += 1
                current_col = 1
            else:
                current_col += 1

            i += 1

        # Reset position if no valid JSON found
        self.line = start_line
        self.column = start_col
        return "", False

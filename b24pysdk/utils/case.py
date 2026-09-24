import re
from typing import Text

__all__ = [
    "camel_to_snake",
    "camel_to_upper",
    "snake_to_camel",
    "upper_to_camel",
]


_CAMEL_WORD_BOUNDARY: re.Pattern = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_LETTER_BOUNDARY: re.Pattern = re.compile(r"([a-z0-9])([A-Z])")


def camel_to_snake(value: Text, /) -> Text:
    """Convert a camelCase or PascalCase name to snake_case."""
    value = _CAMEL_WORD_BOUNDARY.sub(r"\1_\2", value)
    return _CAMEL_LETTER_BOUNDARY.sub(r"\1_\2", value).lower()


def camel_to_upper(value: Text, /) -> Text:
    """Convert a camelCase or PascalCase name to UPPER_SNAKE_CASE."""
    return camel_to_snake(value).upper()


def snake_to_camel(value: Text, /) -> Text:
    """Convert a snake_case name to camelCase."""
    first_word, *other_words = value.split("_")
    return first_word + "".join(word.capitalize() for word in other_words)


def upper_to_camel(value: Text, /) -> Text:
    """Convert an UPPER_SNAKE_CASE name to camelCase."""
    return snake_to_camel(value.lower())

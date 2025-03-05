import re

def is_identifier(symbol: str) -> str | None:
    """Checks if the given word is a valid identifier."""
    return "Identifier" if re.fullmatch(r'^#[A-Za-z][A-Za-z\d]*$', symbol) else None

def is_string_constant(symbol: str) -> str | None:
    """Checks if the given word is a valid string constant."""
    return "String Constant" if re.fullmatch(r'["\'].*?["\']', symbol) else None  # Matches anything between quotes

def is_number_constant(symbol: str) -> str | None:
    """Checks if the given word is a valid number constant (integer or float)."""
    return "Number Constant" if re.fullmatch(r'[+-]?\d+(\.\d+)?', symbol) else None

def is_char_constant(symbol: str) -> str | None:
    """Checks if the given word is a valid character constant (single char in single quotes)."""
    return "Char Constant" if re.fullmatch(r"'.{1}'", symbol) else None

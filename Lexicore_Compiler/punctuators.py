def get_matching_punctuation(symbol: str) -> str | None:
    return punctuators.get(symbol, None)

punctuators = dict([
    ("(", "("),
    (")", ")"),
    ("{", "{"),
    ("}", "}"),
    ("[", "["),
    ("]", "]"),
    (".", "."),
    (",", ","),
    (":", ":"),
    (";", ";"),
    ("?", "?")
])

# Example usage
# print(get_matching_punctuation("("))  # Output: "("

import os
from keywords import get_matching_keywords as gmk
from operators import get_matching_operation as gmo
from punctuators import get_matching_punctuation as gmp
import token_validator as tv
from tabulate import tabulate


class Token:
    """Represents a token with a type, value, and line number."""

    def __init__(self, token_type, value, line_number):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number

    def __str__(self):
        return f"Token Type: {self.token_type}, Value: {self.value}, Line Number: {self.line_number}"


class Lexer:
    """Lexer that processes the source code and breaks it into tokens."""

    digit_set = set("0123456789")
    punctuators = {
        ",",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        ":",
        ";",
        "?",
        "."
    }
    single_length_op = {
        "+",
        "-",
        "*",
        "/","%", "^", "=", "<", ">"}
    compound_symbols = {"!=", "==", "<=", ">=", "+=", "-=", "*=", "/=", "%="}

    def __init__(self, file_content):
        """Initializes the lexer with the source code and other necessary variables."""
        self.file_content = file_content
        self.cursor = 0
        self.line_number = 1

    def word_breaker(self):
        """Breaks the source code into words (tokens)."""
        temp = ""
        in_string = in_char = False
        string_delimiter = ""

        while self.cursor < len(self.file_content):
            curr_char = self.file_content[self.cursor]
            
            # Handling Punctuators
            if curr_char in self.punctuators:
                if temp:
                    return temp, self.cursor, self.line_number
                self.cursor += 1
                return curr_char, self.cursor, self.line_number

            # New line Character
            if curr_char == "\n":
                if temp:
                    return temp, self.cursor, self.line_number
                self.line_number += 1
                self.cursor += 1
                continue

            # Space Character
            if curr_char == " " and not in_string and not in_char:
                self.cursor += 1
                if temp:
                    return temp, self.cursor, self.line_number
                continue

            # String & Character Literals
            if curr_char in {'"', "'"}:
                if not in_string and not in_char:
                    in_string = True
                    string_delimiter = curr_char
                    temp += curr_char
                elif in_string and curr_char == string_delimiter:
                    in_string = False
                    temp += curr_char
                    self.cursor += 1
                    return temp, self.cursor, self.line_number
                else:
                    temp += curr_char
                self.cursor += 1
                continue

            # If inside string, keep collecting characters
            if in_string:
                if curr_char == "\\" and self.cursor + 1 < len(self.file_content):
                    # Handle Escape Sequences properly
                    next_char = self.file_content[self.cursor + 1]
                    if next_char in {'"', "'", "n", "t", "r", "\\"}:
                        temp += curr_char + next_char
                        self.cursor += 2
                        continue
                temp += curr_char
                self.cursor += 1
                continue

            # Floating-Point Numbers Handling
            if curr_char == ".":
                if temp.isdigit():
                    if (
                        self.cursor + 1 < len(self.file_content)
                        and self.file_content[self.cursor + 1] in self.digit_set
                    ):
                        temp += curr_char
                        self.cursor += 1
                        continue
                    else:
                        return temp, self.cursor, self.line_number
                elif not temp:
                    if (
                        self.cursor + 1 < len(self.file_content)
                        and self.file_content[self.cursor + 1] in self.digit_set
                    ):
                        temp += curr_char
                        self.cursor += 1
                        continue
                    else:
                        return ".", self.cursor + 1, self.line_number
                
            # Single-line comments : ~
            if curr_char == "~":
                if temp:
                    return temp, self.cursor, self.line_number
                self.cursor = self.skip_line_comment()
                continue

            # Multi-line comments : $ - $
            if curr_char == "$":
                if temp:
                    return temp, self.cursor, self.line_number
                self.cursor = self.skip_multiline_comment()
                continue


            # Double_length Operation
            if curr_char in {"!", "=", "<", ">", "+", "-", "*", "/", "%"}:
                if self.cursor + 1 < len(self.file_content):
                    next_char = self.file_content[self.cursor + 1]
                    formed_operators = curr_char + next_char

                    if formed_operators in self.compound_symbols:
                        if temp:  # If there was a previous token, return it first
                            return temp, self.cursor, self.line_number

                        self.cursor += 2
                        return formed_operators, self.cursor, self.line_number



            # raw characters
            temp += curr_char
            self.cursor += 1

        if temp:  # Ensure the last token is returned
            return temp, self.cursor, self.line_number

        return None, self.cursor, self.line_number  # End of file case

    def skip_line_comment(self):
        """Skips single-line comments (~)."""
        while (
            self.cursor < len(self.file_content)
            and self.file_content[self.cursor] != "\n"
        ):
            self.cursor += 1
        return self.cursor

    def skip_multiline_comment(self):
        """Skips multi-line comments ($ ... $)."""
        self.cursor += 1  # Skip the opening $
        while (
            self.cursor < len(self.file_content)
            and self.file_content[self.cursor] != "$"
        ):
            if self.file_content[self.cursor] == "\n":
                self.line_number += 1
            self.cursor += 1
        if (
            self.cursor < len(self.file_content)
            and self.file_content[self.cursor] == "$"
        ):
            self.cursor += 1  # Skip the closing $
        return self.cursor


def validate_word(word):
    """Validates a word and returns its type (keyword, operation, etc.)."""
    if not word:
        return "Invalid lexeme"

    if tv.is_char_constant(word):  
        return "Character Constant"  

    if tv.is_string_constant(word):  
        return "String Constant"  

    token_type = (
        gmk(word)
        or gmo(word)
        or gmp(word)
        or tv.is_number_constant(word)
        or tv.is_identifier(word)  
    )

    return token_type if token_type else "Invalid lexeme"



def lexical_analysis(file_content):
    """Performs lexical analysis on the file content."""
    lexer = Lexer(file_content)
    tokens = []

    while lexer.cursor < len(file_content):
        temp, lexer.cursor, lexer.line_number = lexer.word_breaker()

        if temp is None:  # Skip empty tokens
            continue

        token_type = validate_word(temp)
        token = Token(token_type, temp, lexer.line_number)
        tokens.append((token.value, token.token_type, token.line_number))

    return tokens


def print_tokens(tokens):
    """Prints the token set in a well-formatted tabular style."""
    headers = ["Token Value", "Token Type", "Line Number"]
    print("\nLexical Analysis Output:\n")
    print(tabulate(tokens, headers=headers, tablefmt="fancy_grid"))


def main():
    """Main function that reads the file and performs lexical analysis."""
    source_file_name = input("Enter file name (without extension) = ") + ".txt"

    if not os.path.exists(source_file_name):
        open(source_file_name, "w").close()
        print(
            f"File '{source_file_name}' created successfully. Now go and code first!!"
        )
    else:
        with open(source_file_name, "r") as file:
            file_content = file.read()
            tokens = lexical_analysis(file_content)
            print_tokens(tokens)  # Display tokens in a clean table


if __name__ == "__main__":
    main()

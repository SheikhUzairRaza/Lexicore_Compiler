def get_matching_operation(symbol: str) -> str | None:
    return operators.get(symbol, None)

operators = dict([
    ("+", "ASDOP"),    # Addition
    ("-", "ASDOP"),    # Subtraction
    
    ("*", "APDR"),     # Multiplication(Aritmetic Product Division Remainder)
    ("/", "APDR"),     # Division
    ("%", "APDR"),     # Modulo
    
    ("<", "RO1"),      # Less than
    (">", "RO1"),      # Greater than
    ("<=", "RO1"),     # Less than or equal
    (">=", "RO1"),     # Greater than or equal 
    
    ("!=", "RO2"),     # Not equal 
    ("==", "RO2"),     # Equal
    
    ("!", "LO1"),       # Logical NOT
    
    ("=", "="),        # Assignment
    
    ("+=", "CAOP"),    # Add and assign
    ("-=", "CAOP"),    # Subtract and assign
    ("*=", "CAOP"),    # Multiply and assign
    ("/=", "CAOP"),    # Divide and assign
    ("%=", "CAOP"),    # Modulo and assign
    
    ("&&", "LO2"),     # Logical AND
    ("||", "LO2"),     # Logical OR
])



# print(get_matching_operation(("*=")))

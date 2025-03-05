def get_matching_keywords(symbol : str)->str | None:
    return keywords.get(symbol,None)
       
keywords = dict([
    ("hold", "let"),
    ("freeze", "const"),
    ("from","from"),
    ("step","step"),
    ("to","to"),
    ("as","as"),
    ("num", "DT"),  # num indicates int,float,double,short,long DT
    ("enum", "enum"),
    ("flag", "DT"), # flag indicates bool DT
    ("char", "DT"),
    ("word", "string"),
    ("using","using"),
    ("with","with"),
    ("execute","execute"),
    ("recur", "recur"),
    ("verify", "if"),
    ("retry", "elif"),
    ("default", "else"),
    ("yield", "return"),
    ("True", "boolean"),
    ("False", "boolean"),
    ("discontinue", "controlFlow"), 
    ("continue", "controlFlow"),     
    ("void", "void"),
    ("say", "print"),
    ("model", "class"),
    ("instantiate", "new"),
    ("null", "null"),
    ("extend", "extend"),
    ("implement", "implement"),
    ("static", "static"),
    ("final", "final"),
    ("open", "AS"), #open indicates Public Access Specifier
    ("hide", "AS"), #hide indicates Private Access Specifier
    ("safe", "AS"), #safe indicates Protected Access Specifier
    ("fun", "fun")
])

# print(get_matching_keywords("safe"))
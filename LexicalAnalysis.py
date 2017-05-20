import re
# Defining set of lexemes
operators = {"+": "Add operator", "-": "Sub operator", "*": "Mul operator", "/": "Div operator", "%": "Modulo operator",
             "<": "less than operator", ">": "greater than operator", "=": "assignment operator"}
types = {"int": "Integer datatype", "float": "Float datatype", "char": "Character datatype",
         "double": "Double datatype", "void": "void return type"}
keywords = {"if()": "if conditional statement", "else": "else conditional statement", "for()": "for loop",
            "while()": "while loop", "return": "return statement"}
symbols = {}
output_lines = []

input_code = list(line.strip() for line in open("lexical_input.c"))

for line in input_code:
    if "#include" in line:  # Ignore #include statements
        continue

    line = re.sub("\(.*\)", "()", line)  # Remove everything with parenthesis
    line = line.replace("{", " ")  # Remove braces
    line = line.replace("}", " ")  # Remove braces
    split_line = re.split("([\s,\+\-\*\/\%\;\=])", line)  # Split on multiple delimiters
    split_line = list(filter((lambda x: x != "" and x != " " and x != ";" and x != ","),
                             split_line))  # Remove spaces commas semicolons
    output = []
    for token in split_line:
        token = token.strip()
        if token in operators.keys():
            output.append({token: operators[token]})
        elif token in keywords.keys():
            output.append({token: keywords[token]})
        elif token in types.keys():
            output.append(({token:types[token]}))
        elif token.isdigit():
            output.append({token:"Numerical constant"})
        elif re.match("\".*\"",token):
            output.append({token:"String constant"})
        elif re.match("\'.\'", token):
            output.append({token: "Character constant"})
        elif re.match(".*\(.*\)", token):
            output.append({token: "function"})
        else:
            if token not in symbols.keys():
                symbols[token] = "id" + str(len(symbols))
            output.append({token: symbols[token]})
    output_lines.append(output)

for line in output_lines:
    print(line)
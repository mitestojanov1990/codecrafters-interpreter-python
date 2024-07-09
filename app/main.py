import sys


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Uncomment this block to pass the first stage
    if file_contents:
        res = scan_string(file_contents)

    print("EOF  null")  # Placeholder, remove this line when implementing the scanner
    if file_contents and res:
        exit(65)


def scan_string(text):
    line_number = 1
    has_error = False
    for i, c in enumerate(text):
        if c == "\n":
            line_number += 1
        elif c in "!=<>":
            if i + 1 < len(text) and text[i + 1] == "=":
                operator_sign = readable_names_for_operators.setdefault(c + "=", None)
                print(f"{operator_sign} {c}= null")
                i += 1
            else:
                operator_sign = readable_names_for_operators.setdefault(c, None)
                print(f"{operator_sign} {c} null")

        else:
            ascii_value = ord(c)
            if ascii_value in readable_names_for_tokens:
                sign = readable_names_for_tokens.setdefault(ascii_value, None)
                print(f"{sign} {chr(ascii_value)} null")
            else:
                print(
                    f"[line {line_number}] Error: Unexpected character: {c}",
                    file=sys.stderr,
                )
                has_error = True
        i += 1
    return has_error


readable_names_for_operators = {
    "=": "EQUAL",
    ">=": "GREATER_EQUAL",
    "<=": "LESS_EQUAL",
    "==": "EQUAL_EQUAL",
    "!=": "BANG_EQUAL",
}

readable_names_for_tokens = {
    40: "LEFT_PAREN",
    41: "RIGHT_PAREN",
    42: "STAR",
    43: "PLUS",
    44: "COMMA",
    45: "MINUS",
    46: "DOT",
    59: "SEMICOLON",
    61: "EQUAL",
    123: "LEFT_BRACE",
    125: "RIGHT_BRACE",
}
single_character_tokens = {
    40: "(",
    41: ")",
    42: "*",
    43: "+",
    44: ",",
    45: "-",
    46: ".",
    # 47: '/'
    59: ";",
    61: "=",
    123: "{",
    125: "}",
}


if __name__ == "__main__":
    main()

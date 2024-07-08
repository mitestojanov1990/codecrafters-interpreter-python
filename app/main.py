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
        scan_string(file_contents)

    print("EOF  null")  # Placeholder, remove this line when implementing the scanner


def my_printer(text):
    print(text)


def scan_characters(c):
    scan_parentheses(c)
    scan_braces(c)


def scan_parentheses(c):
    if "(" == c:
        my_printer("LEFT_PAREN ( null")
    elif ")" == c:
        my_printer("RIGHT_PAREN ) null")
    else:
        return


def scan_braces(c):
    if "{" == c:
        my_printer("LEFT_BRACE { null")
    elif "}" == c:
        my_printer("RIGHT_BRACE } null")


def scan_string(text):
    [print(get_print_name(ord(c))) for c in text]


def get_print_name(ascii):

    sign = readable_names_for_tokens.setdefault(ascii, None)
    if sign is not None:
        return f"{sign} {chr(ascii)} null"
    else:
        return f"[line 1] Error: Unexpected character: {chr(ascii)}"


readable_names_for_tokens = {
    40: "LEFT_PAREN",
    41: "RIGHT_PAREN",
    42: "STAR",
    43: "PLUS",
    44: "COMMA",
    45: "MINUS",
    46: "DOT",
    59: "SEMICOLON",
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
    123: "{",
    125: "}",
}


if __name__ == "__main__":
    main()

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
        [scan_characters(c) for c in file_contents]

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
        my_printer("LEFT_BRACE ( null")
    elif "}" == c:
        my_printer("RIGHT_BRACE ) null")


if __name__ == "__main__":
    main()

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
        return [scan_parentheses(item) for item in file_contents]
        raise NotImplementedError("Scanner not implemented")
    else:
        print(
            "EOF  null"
        )  # Placeholder, remove this line when implementing the scanner


def scan_parentheses(item):
    if "(":
        return "LEFT_PAREN ( null"
    elif ")":
        return "RIGHT_PAREN ) null"
    else:
        return "EOF null"


if __name__ == "__main__":
    main()

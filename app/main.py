from enum import Enum
import sys


def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except FileNotFoundError:
        print(f"[line 1] Error: File not found: {filename}", file=sys.stderr)
        exit(65)

    scanner = Scanner(file_contents)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token.to_string())
    print("EOF  null")
    if scanner.has_errors:
        exit(65)


TokenType = Enum(
    "TokenType",
    [
        "LEFT_PAREN",
        "RIGHT_PAREN",
        "LEFT_BRACE",
        "RIGHT_BRACE",
        "COMMA",
        "DOT",
        "MINUS",
        "PLUS",
        "SEMICOLON",
        "SLASH",
        "STAR",
        "BANG",
        "BANG_EQUAL",
        "EQUAL",
        "EQUAL_EQUAL",
        "GREATER",
        "GREATER_EQUAL",
        "LESS",
        "LESS_EQUAL",
        "EOF",
        "STRING",
        "NUMBER",
        "IDENTIFIER",
        "AND",
        "CLASS",
        "ELSE",
        "FALSE",
        "FUN",
        "FOR",
        "IF",
        "NIL",
        "OR",
        "PRINT",
        "RETURN",
        "SUPER",
        "THIS",
        "TRUE",
        "VAR",
        "WHILE",
    ],
)
keywords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "fun": TokenType.FUN,
    "for": TokenType.FOR,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


class Token:
    def __init__(self, token_type: str, lexeme, literal, line):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.token_type.name} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.has_errors = False

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        # self.tokens.append(Token(TokenType.EOF, "", "null", self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token_without_literal(TokenType.LEFT_PAREN)
            case ")":
                self.add_token_without_literal(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token_without_literal(TokenType.LEFT_BRACE)
            case "}":
                self.add_token_without_literal(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token_without_literal(TokenType.COMMA)
            case ".":
                self.add_token_without_literal(TokenType.DOT)
            case "-":
                self.add_token_without_literal(TokenType.MINUS)
            case "+":
                self.add_token_without_literal(TokenType.PLUS)
            case ";":
                self.add_token_without_literal(TokenType.SEMICOLON)
            case "*":
                self.add_token_without_literal(TokenType.STAR)
            case "!":
                self.add_token_without_literal(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token_without_literal(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token_without_literal(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token_without_literal(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token_without_literal(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass  # Ignore whitespace
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha() or c == "_":
                    self.identifier()
                else:
                    print(
                        f"[line {self.line}] Error: Unexpected character: {c}",
                        file=sys.stderr,
                    )
                    self.has_errors = True

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start : self.current]
        token_type = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type, "null")

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
            self.has_errors = True
            return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def is_at_end(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type, literal):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def add_token_without_literal(self, token_type):
        self.add_token(token_type, "null")


if __name__ == "__main__":
    main()

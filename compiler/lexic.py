import string 

from compiler.errors import LexicalError
from compiler.token import (
    RESERVED_WORDS,
    DOUBLE_OPERATORS,
    SIMPLE_SYMBOLS,
    TokenType,
    Token
)

LETTERS = set(string.ascii_letters + "_")
DIGITS = set(string.digits)

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.tokens = []                   

    def actual(self):
        if self.pos < len(self.text):
            return self.text[self.pos]

        return ""

    def peek(self):                         
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]

        return ""

    def add(self, type, lexeme):
        self.tokens.append(Token(type, lexeme, self.line))
        

    def tokenize(self):
        while self.pos < len(self.text):
            c = self.actual()

            if c in " \t\r":               
                self.pos += 1

            elif c == "\n":
                self.line += 1
                self.pos += 1

            elif c == "#":                  
                self.skip_comment()
        
            elif c in LETTERS:
                self.read_word()
        
            elif c in DIGITS:
                self.read_number()
        
            elif c == '"':
                self.read_text()

            elif c == "'":
                self.read_char()

            else:
                self.read_simbol()
        
        self.add(TokenType.EOF, "")        
        return self.tokens

    def skip_comment(self):               
        while self.actual() not in ("\n", ""):
            self.pos += 1

    def read_word(self):
        start = self.pos

        while self.actual() in LETTERS or self.actual() in DIGITS:  
            self.pos += 1

        word = self.text[start:self.pos]

        type = RESERVED_WORDS.get(word, TokenType.IDENTIFIER)

        self.add(type, word)

    def read_number(self):
        start = self.pos

        while self.actual() in DIGITS:
            self.pos += 1

        type = TokenType.LIT_INT         

        if self.actual() == "." and self.peek() in DIGITS:
            type = TokenType.LIT_FLOAT     

            self.pos += 1

            while self.actual() in DIGITS:
                self.pos += 1

        if self.actual() in LETTERS:
             raise LexicalError(self.line, f"invalid character in number '{self.text[start: self.pos + 1]}'")

        self.add(type, self.text[start:self.pos])


    def read_text(self):
        start = self.pos
        self.pos += 1

        while self.actual() != '"':
            if self.actual() in ('\n', ''):
                raise LexicalError(self.line, "unterminated string literal")

            self.pos += 1

        self.pos += 1
        self.add(TokenType.LIT_STR, self.text[start:self.pos])

    def read_char(self):
        start = self.pos
        self.pos += 1

        if self.actual() == "'":
            raise LexicalError(self.line, "empty character literal")

        if self.actual() in ("\n", ""):
            raise LexicalError(self.line, "unterminated character literal")

        if not self.actual().isascii():
            raise LexicalError(self.line, f"character literal must be an ASCII character, found '{self.actual()}'")

        self.pos += 1

        if self.actual() != "'":
            raise LexicalError(self.line, "character literal must contain exactly one character")

        self.pos += 1
        self.add(TokenType.LIT_CHAR, self.text[start:self.pos])

    def read_simbol(self):
        two = self.text[self.pos: self.pos + 2]

        if two in DOUBLE_OPERATORS:
            self.add(DOUBLE_OPERATORS[two], two)
            self.pos += 2

        elif self.actual() in SIMPLE_SYMBOLS:
            self.add(SIMPLE_SYMBOLS[self.actual()], self.actual())
            self.pos += 1

        else:
            raise LexicalError(self.line, f"invalid character '{self.actual()}'")

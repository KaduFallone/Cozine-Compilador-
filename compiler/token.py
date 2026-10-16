from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    PANELA = auto()
    ACENDERFOGAO = auto()
    LIQUIDIFICAR = auto()
    FLAMBAR = auto()
    EM = auto()        
    RANGE = auto()
    GARFO = auto()
    COLHER = auto()       
    FACA = auto()
    RECEITA = auto()      
    COMER = auto()
    INT = auto()           
    FLOAT = auto()
    STR = auto()
    CHAR = auto()
    IDENTIFIER = auto()    
    LIT_INT = auto()       
    LIT_FLOAT = auto()
    LIT_STR = auto()
    LIT_CHAR = auto()
    BIGGER = auto()
    SMALLER = auto()
    EQUAL = auto()
    DIFFERENT = auto()
    BIGGEREQUAL = auto()
    SMALLEREQUAL = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    ASSIGN = auto()        
    ARROW = auto()        
    COLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    EOF = auto()           


RESERVED_WORDS = {
    "panela": TokenType.PANELA,
    "acenderfogao": TokenType.ACENDERFOGAO,
    "liquidificar": TokenType.LIQUIDIFICAR,
    "flambar": TokenType.FLAMBAR,
    "em": TokenType.EM,
    "range": TokenType.RANGE,
    "garfo": TokenType.GARFO,
    "colher": TokenType.COLHER,
    "faca": TokenType.FACA,
    "receita": TokenType.RECEITA,
    "comer": TokenType.COMER,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "str": TokenType.STR,
    "char": TokenType.CHAR,
}

DOUBLE_OPERATORS ={
    ">=": TokenType.BIGGEREQUAL,
    "<=": TokenType.SMALLEREQUAL,
    "==": TokenType.EQUAL,
    "!=": TokenType.DIFFERENT,
    "->": TokenType.ARROW,
}

SIMPLE_SYMBOLS = {
    ">": TokenType.BIGGER,
    "<": TokenType.SMALLER,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "=": TokenType.ASSIGN,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    ";": TokenType.SEMICOLON,
}


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int             

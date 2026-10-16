from compiler.ast_nodes import (
    Assign,
    BinaryOp,
    Call,
    CallStatement,
    CharLiteral,
    Condition,
    FloatLiteral,
    For,
    FuncDecl,
    Group,
    If,
    IfBranch,
    IntLiteral,
    Param,
    Print,
    Program,
    Return,
    StrLiteral,
    UnaryOp,
    Variable,
    VarDecl,
    While,
)
from compiler.errors import SyntacticError
from compiler.token import DOUBLE_OPERATORS, RESERVED_WORDS, SIMPLE_SYMBOLS, TokenType

TOKEN_TEXT = {
    token_type: f"'{text}'"
    for text, token_type in {**RESERVED_WORDS, **DOUBLE_OPERATORS, **SIMPLE_SYMBOLS}.items()
}

TYPE_NAMES = {
    TokenType.INT: "int",
    TokenType.FLOAT: "float",
    TokenType.STR: "str",
    TokenType.CHAR: "char",
}

COMPARISONS = (
    TokenType.EQUAL,
    TokenType.DIFFERENT,
    TokenType.BIGGER,
    TokenType.SMALLER,
    TokenType.BIGGEREQUAL,
    TokenType.SMALLEREQUAL,
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos]

    def peek(self):
        return self.tokens[min(self.pos + 1, len(self.tokens) - 1)]

    def check(self, *types):
        return self.actual().type in types

    def advance(self):
        token = self.actual()

        if token.type != TokenType.EOF:
            self.pos += 1

        return token

    def error(self, expected):
        token = self.actual()
        found = "end of file" if token.type == TokenType.EOF else f"'{token.lexeme}'"

        if self.pos == 0:
            raise SyntacticError(token.line, f"expected {expected}, found {found}")

        previous = self.tokens[self.pos - 1]
        raise SyntacticError(previous.line, f"expected {expected} after '{previous.lexeme}', found {found}")

    def expect(self, type, expected=None):
        if not self.check(type):
            self.error(expected or TOKEN_TEXT[type])

        return self.advance()

    def parse_program(self):
        statements = []

        while not self.check(TokenType.EOF):
            statements.append(self.parse_statement())

        return Program(statements)

    def parse_statement(self):
        token = self.actual()

        if token.type == TokenType.PANELA:
            return self.parse_declaration()

        if token.type == TokenType.ACENDERFOGAO:
            return self.parse_print()

        if token.type == TokenType.GARFO:
            return self.parse_if()

        if token.type == TokenType.LIQUIDIFICAR:
            return self.parse_while()

        if token.type == TokenType.FLAMBAR:
            return self.parse_for()

        if token.type == TokenType.RECEITA:
            return self.parse_function()

        if token.type == TokenType.COMER:
            return self.parse_return()

        if token.type == TokenType.IDENTIFIER:
            if self.peek().type == TokenType.ASSIGN:
                return self.parse_assignment()

            if self.peek().type == TokenType.LPAREN:
                return self.parse_call_statement()

            self.advance()
            self.error("'=' or '('")

        if token.type in (TokenType.COLHER, TokenType.FACA):
            raise SyntacticError(token.line, f"'{token.lexeme}' without a 'garfo' before it")

        found = "end of file" if token.type == TokenType.EOF else f"'{token.lexeme}'"
        raise SyntacticError(token.line, f"a command cannot start with {found}")

    def parse_declaration(self):
        line = self.advance().line
        name = self.expect(TokenType.IDENTIFIER, "a variable name").lexeme
        self.expect(TokenType.COLON)
        type_name = self.parse_type()
        value = None

        if self.check(TokenType.ASSIGN):
            self.advance()
            value = self.parse_expression()

        self.expect(TokenType.SEMICOLON)
        return VarDecl(name, type_name, value, line)

    def parse_type(self):
        if self.actual().type not in TYPE_NAMES:
            self.error("a type (int, float, str or char)")

        return TYPE_NAMES[self.advance().type]

    def parse_assignment(self):
        token = self.advance()
        self.advance()
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assign(token.lexeme, value, token.line)

    def parse_call_statement(self):
        call = self.parse_call()
        self.expect(TokenType.SEMICOLON)
        return CallStatement(call, call.line)

    def parse_print(self):
        line = self.advance().line
        self.expect(TokenType.LPAREN)
        args = self.parse_arguments()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return Print(args, line)

    def parse_if(self):
        line = self.advance().line
        branches = [IfBranch(self.parse_condition(), self.parse_block(), line)]

        while self.check(TokenType.COLHER):
            colher_line = self.advance().line
            branches.append(IfBranch(self.parse_condition(), self.parse_block(), colher_line))

        else_body = None

        if self.check(TokenType.FACA):
            self.advance()
            else_body = self.parse_block()

            if self.check(TokenType.COLHER):
                raise SyntacticError(self.actual().line, "'colher' cannot come after 'faca'")

        self.expect(TokenType.SEMICOLON)
        return If(branches, else_body, line)

    def parse_while(self):
        line = self.advance().line
        condition = self.parse_condition()
        body = self.parse_block()
        self.expect(TokenType.SEMICOLON)
        return While(condition, body, line)

    def parse_for(self):
        line = self.advance().line
        self.expect(TokenType.LPAREN)
        var = self.expect(TokenType.IDENTIFIER, "the counter name").lexeme
        self.expect(TokenType.EM)
        self.expect(TokenType.RANGE)
        self.expect(TokenType.LPAREN)
        start = self.parse_expression()
        self.expect(TokenType.COMMA)
        end = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        self.expect(TokenType.SEMICOLON)
        return For(var, start, end, body, line)

    def parse_function(self):
        line = self.advance().line
        name = self.expect(TokenType.IDENTIFIER, "the receita name").lexeme
        self.expect(TokenType.LPAREN)
        params = []

        if not self.check(TokenType.RPAREN):
            params.append(self.parse_param())

            while self.check(TokenType.COMMA):
                self.advance()
                params.append(self.parse_param())

        self.expect(TokenType.RPAREN)
        return_type = None

        if self.check(TokenType.ARROW):
            self.advance()
            return_type = self.parse_type()

        body = self.parse_block()
        self.expect(TokenType.SEMICOLON)
        return FuncDecl(name, params, return_type, body, line)

    def parse_param(self):
        token = self.expect(TokenType.IDENTIFIER, "a parameter name")
        self.expect(TokenType.COLON)
        return Param(token.lexeme, self.parse_type(), token.line)

    def parse_return(self):
        line = self.advance().line
        value = None

        if not self.check(TokenType.SEMICOLON):
            value = self.parse_expression()

        self.expect(TokenType.SEMICOLON)
        return Return(value, line)

    def parse_block(self):
        opening = self.expect(TokenType.LBRACE)
        statements = []

        while not self.check(TokenType.RBRACE, TokenType.EOF):
            statements.append(self.parse_statement())

        if self.check(TokenType.EOF):
            raise SyntacticError(opening.line, "'{' was not closed with '}'")

        self.advance()
        return statements

    def parse_condition(self):
        self.expect(TokenType.LPAREN)
        left = self.parse_expression()

        if not self.check(*COMPARISONS):
            self.error("a comparison operator (==, !=, <, >, <=, >=)")

        operator = self.advance()
        right = self.parse_expression()
        self.expect(TokenType.RPAREN)
        return Condition(operator.lexeme, left, right, operator.line)

    def parse_expression(self):
        node = self.parse_term()

        while self.check(TokenType.PLUS, TokenType.MINUS):
            operator = self.advance()
            node = BinaryOp(operator.lexeme, node, self.parse_term(), operator.line)

        return node

    def parse_term(self):
        node = self.parse_unary()

        while self.check(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.advance()
            node = BinaryOp(operator.lexeme, node, self.parse_unary(), operator.line)

        return node

    def parse_unary(self):
        if self.check(TokenType.MINUS):
            operator = self.advance()
            return UnaryOp("-", self.parse_unary(), operator.line)

        return self.parse_factor()

    def parse_factor(self):
        token = self.actual()

        if token.type == TokenType.LIT_INT:
            self.advance()
            return IntLiteral(int(token.lexeme), token.line)

        if token.type == TokenType.LIT_FLOAT:
            self.advance()
            return FloatLiteral(token.lexeme, token.line)

        if token.type == TokenType.LIT_STR:
            self.advance()
            return StrLiteral(token.lexeme[1:-1], token.line)

        if token.type == TokenType.LIT_CHAR:
            self.advance()
            return CharLiteral(token.lexeme[1:-1], token.line)

        if token.type == TokenType.IDENTIFIER:
            if self.peek().type == TokenType.LPAREN:
                return self.parse_call()

            self.advance()
            return Variable(token.lexeme, token.line)

        if token.type == TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return Group(expression, token.line)

        self.error("a value (number, text, character, name or '(')")

    def parse_call(self):
        token = self.advance()
        self.expect(TokenType.LPAREN)
        args = []

        if not self.check(TokenType.RPAREN):
            args = self.parse_arguments()

        self.expect(TokenType.RPAREN)
        return Call(token.lexeme, args, token.line)

    def parse_arguments(self):
        args = [self.parse_expression()]

        while self.check(TokenType.COMMA):
            self.advance()
            args.append(self.parse_expression())

        return args

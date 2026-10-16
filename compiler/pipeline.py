from compiler.generator import CodeGenerator
from compiler.lexic import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer


def compile_source(code):
    tokens = Lexer(code).tokenize()
    program = Parser(tokens).parse_program()
    table = SemanticAnalyzer().analyze(program)
    return CodeGenerator(table).generate(program)

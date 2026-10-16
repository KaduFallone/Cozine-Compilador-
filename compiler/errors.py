class CompilationError(Exception):
    stage = 'compilation'

    def __init__ (self, line, reason):
        super().__init__(f'{self.stage.capitalize()} error at line {line}: {reason}')
        self.line = line
        self.reason = reason

class LexicalError(CompilationError):
    stage = 'lexical'

class SyntacticError(CompilationError):
    stage = 'syntactic'

class SemanticError(CompilationError):
    stage = 'semantic'

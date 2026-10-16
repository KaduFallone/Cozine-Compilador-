from dataclasses import dataclass, field

from compiler.errors import SemanticError

GLOBAL = "global"


@dataclass
class Symbol:
    name: str
    kind: str
    type: str
    scope: str
    line: int
    initialized: bool = False
    params: list = field(default_factory=list)


class SymbolTable:
    def __init__(self):
        self.scopes = {GLOBAL: {}}
        self.current = GLOBAL
        self.symbols = []

    def declare(self, symbol):
        scope = self.scopes[self.current]

        if symbol.name in scope:
            raise SemanticError(symbol.line, f"'{symbol.name}' was already declared at line {scope[symbol.name].line}")

        outer = self.scopes[GLOBAL].get(symbol.name)

        if outer is not None and outer.kind == "receita":
            raise SemanticError(symbol.line, f"'{symbol.name}' is already the name of a receita")

        scope[symbol.name] = symbol
        self.symbols.append(symbol)
        return symbol

    def declare_variable(self, name, type, line, initialized):
        return self.declare(Symbol(name, "variable", type, self.current, line, initialized))

    def declare_parameter(self, name, type, line):
        return self.declare(Symbol(name, "parameter", type, self.current, line, True))

    def declare_function(self, name, param_types, return_type, line):
        return self.declare(Symbol(name, "receita", return_type, self.current, line, True, list(param_types)))

    def enter_function(self, name):
        self.scopes[name] = {}
        self.current = name

    def exit_function(self):
        self.current = GLOBAL

    def lookup(self, name):
        symbol = self.scopes[self.current].get(name)

        if symbol is None and self.current != GLOBAL:
            outer = self.scopes[GLOBAL].get(name)

            if outer is not None and outer.kind == "receita":
                symbol = outer

        return symbol

    def lookup_global(self, name):
        return self.scopes[GLOBAL].get(name)

    def initialized_names(self):
        return {name for name, symbol in self.scopes[self.current].items() if symbol.initialized}

    def restore_initialized(self, names):
        for name, symbol in self.scopes[self.current].items():
            if symbol.kind == "variable" and name not in names:
                symbol.initialized = False

    def format(self):
        header = f"{'NAME':<15} {'KIND':<10} {'TYPE':<22} {'SCOPE':<12} {'INITIALIZED':<12} LINE"
        rows = [header, "-" * len(header)]

        for symbol in self.symbols:
            type_text = symbol.type
            initialized = "yes" if symbol.initialized else "no"

            if symbol.kind == "receita":
                type_text = f"({', '.join(symbol.params)}) -> {symbol.type}"
                initialized = "-"

            rows.append(f"{symbol.name:<15} {symbol.kind:<10} {type_text:<22} {symbol.scope:<12} {initialized:<12} {symbol.line}")

        return "\n".join(rows)

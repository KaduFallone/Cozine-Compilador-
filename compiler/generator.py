from compiler.ast_nodes import (
    BinaryOp,
    Call,
    CharLiteral,
    FloatLiteral,
    FuncDecl,
    Group,
    IntLiteral,
    StrLiteral,
    UnaryOp,
    Variable,
)

CPP_TYPES = {
    "int": "int",
    "float": "double",
    "str": "std::string",
    "char": "char",
    None: "void",
}

CPP_RESERVED = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool",
    "break", "case", "catch", "char8_t", "char16_t", "char32_t", "class", "compl",
    "concept", "const", "consteval", "constexpr", "constinit", "const_cast", "continue",
    "co_await", "co_return", "co_yield", "decltype", "default", "delete", "do", "double",
    "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "for",
    "friend", "goto", "if", "inline", "long", "mutable", "namespace", "new", "noexcept",
    "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected",
    "public", "register", "reinterpret_cast", "requires", "return", "short", "signed",
    "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template",
    "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename",
    "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while",
    "xor", "xor_eq", "main", "std", "NULL", "EOF", "stdin", "stdout", "stderr", "errno",
}

INDENT = "    "


class CodeGenerator:
    def __init__(self, table):
        self.used_names = {symbol.name for symbol in table.symbols}
        self.renamed = {}
        self.counter = 0
        self.lines = []
        self.level = 0

    def generate(self, program):
        functions = [s for s in program.statements if isinstance(s, FuncDecl)]
        main_body = [s for s in program.statements if not isinstance(s, FuncDecl)]

        self.lines = ["#include <iostream>", "#include <string>", ""]

        for function in functions:
            self.visit(function)
            self.lines.append("")

        self.emit("int main() {")
        self.body(main_body)
        self.level += 1
        self.emit("return 0;")
        self.level -= 1
        self.emit("}")

        return "\n".join(self.lines) + "\n"

    def emit(self, text):
        self.lines.append(INDENT * self.level + text)

    def body(self, statements):
        self.level += 1

        for statement in statements:
            self.visit(statement)

        self.level -= 1

    def visit(self, node):
        getattr(self, f"visit_{type(node).__name__}")(node)

    def name(self, name):
        if name not in CPP_RESERVED:
            return name

        if name not in self.renamed:
            new_name = f"{name}_cz"

            while new_name in self.used_names:
                new_name += "_"

            self.renamed[name] = new_name
            self.used_names.add(new_name)

        return self.renamed[name]

    def fresh_name(self, base):
        while True:
            self.counter += 1
            candidate = f"{base}_{self.counter}"

            if candidate not in self.used_names:
                self.used_names.add(candidate)
                return candidate

    def visit_VarDecl(self, node):
        text = f"{CPP_TYPES[node.type_name]} {self.name(node.name)}"

        if node.value is not None:
            text += f" = {self.expression(node.value)}"

        self.emit(text + ";")

    def visit_Assign(self, node):
        self.emit(f"{self.name(node.name)} = {self.expression(node.value)};")

    def visit_Print(self, node):
        values = ' << " " << '.join(self.expression(arg) for arg in node.args)
        self.emit(f"std::cout << {values} << std::endl;")

    def visit_If(self, node):
        for position, branch in enumerate(node.branches):
            keyword = "if" if position == 0 else "} else if"
            self.emit(f"{keyword} ({self.condition(branch.condition)}) {{")
            self.body(branch.body)

        if node.else_body is not None:
            self.emit("} else {")
            self.body(node.else_body)

        self.emit("}")

    def visit_While(self, node):
        self.emit(f"while ({self.condition(node.condition)}) {{")
        self.body(node.body)
        self.emit("}")

    def visit_For(self, node):
        var = self.name(node.var)
        start = self.expression(node.start)

        if isinstance(node.end, IntLiteral):
            end = self.expression(node.end)
        else:
            end = self.fresh_name("range_end")
            self.emit(f"const int {end} = {self.expression(node.end)};")

        self.emit(f"for ({var} = {start}; {var} < {end}; {var}++) {{")
        self.body(node.body)
        self.emit("}")

    def visit_FuncDecl(self, node):
        params = ", ".join(f"{CPP_TYPES[p.type_name]} {self.name(p.name)}" for p in node.params)
        self.emit(f"{CPP_TYPES[node.return_type]} {self.name(node.name)}({params}) {{")
        self.body(node.body)
        self.emit("}")

    def visit_Return(self, node):
        if node.value is None:
            self.emit("return;")
        else:
            self.emit(f"return {self.expression(node.value)};")

    def visit_CallStatement(self, node):
        self.emit(f"{self.expression(node.call)};")

    def condition(self, node):
        return f"{self.expression(node.left, True)} {node.operator} {self.expression(node.right, True)}"

    def expression(self, node, in_operation=False):
        if isinstance(node, IntLiteral):
            return str(node.value)

        if isinstance(node, FloatLiteral):
            integer, decimal = node.value.split(".")
            return f"{int(integer)}.{decimal}"

        if isinstance(node, StrLiteral):
            text = '"' + node.value.replace("\\", "\\\\") + '"'
            return f"std::string({text})" if in_operation else text

        if isinstance(node, CharLiteral):
            return "'" + node.value.replace("\\", "\\\\") + "'"

        if isinstance(node, Variable):
            return self.name(node.name)

        if isinstance(node, Group):
            return f"({self.expression(node.expression, in_operation)})"

        if isinstance(node, UnaryOp):
            operand = self.expression(node.operand)

            if isinstance(node.operand, UnaryOp):
                return f"-({operand})"

            return f"-{operand}"

        if isinstance(node, BinaryOp):
            left = self.expression(node.left, True)
            right = self.expression(node.right, True)

            if node.operator == "/":
                return f"static_cast<double>({left}) / {right}"

            return f"{left} {node.operator} {right}"

        if isinstance(node, Call):
            args = ", ".join(self.expression(arg) for arg in node.args)
            return f"{self.name(node.name)}({args})"

        raise TypeError(f"unknown expression: {node}")

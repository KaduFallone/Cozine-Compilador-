from compiler.ast_nodes import (
    BinaryOp,
    Call,
    CharLiteral,
    FloatLiteral,
    Group,
    If,
    IntLiteral,
    Return,
    StrLiteral,
    UnaryOp,
    Variable,
)
from compiler.errors import SemanticError
from compiler.symbol_table import SymbolTable

NUMERIC = ("int", "float")


def assignable(target, value):
    return target == value or (target == "float" and value == "int")


def arithmetic_result(operator, left, right):
    if left in NUMERIC and right in NUMERIC:
        if operator == "/" or "float" in (left, right):
            return "float"
        return "int"

    if operator == "+" and left == right == "str":
        return "str"

    return None


def comparable(left, right):
    if left in NUMERIC and right in NUMERIC:
        return True

    return left == right and left in ("str", "char")


def always_returns(statements):
    for statement in statements:
        if isinstance(statement, Return):
            return True

        if isinstance(statement, If) and statement.else_body is not None:
            branches = [branch.body for branch in statement.branches] + [statement.else_body]

            if all(always_returns(body) for body in branches):
                return True

    return False


class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()
        self.function = None
        self.block_depth = 0

    def analyze(self, program):
        for statement in program.statements:
            self.visit(statement)

        return self.table

    def visit(self, node):
        return getattr(self, f"visit_{type(node).__name__}")(node)

    def block(self, statements):
        before = self.table.initialized_names()
        self.block_depth += 1

        for statement in statements:
            self.visit(statement)

        self.block_depth -= 1
        self.table.restore_initialized(before)

    def visit_VarDecl(self, node):
        if self.block_depth > 0:
            raise SemanticError(node.line, f"variable '{node.name}' cannot be declared inside a block")

        if node.value is not None:
            value_type = self.expression(node.value)

            if not assignable(node.type_name, value_type):
                raise SemanticError(node.line, f"variable '{node.name}' is {node.type_name} and cannot receive a value of type {value_type}")

        self.table.declare_variable(node.name, node.type_name, node.line, node.value is not None)

    def visit_Assign(self, node):
        symbol = self.find_variable(node.name, node.line)
        value_type = self.expression(node.value)

        if not assignable(symbol.type, value_type):
            raise SemanticError(node.line, f"variable '{node.name}' is {symbol.type} and cannot receive a value of type {value_type}")

        symbol.initialized = True

    def visit_Print(self, node):
        for arg in node.args:
            self.expression(arg)

    def visit_If(self, node):
        for branch in node.branches:
            self.condition(branch.condition)
            self.block(branch.body)

        if node.else_body is not None:
            self.block(node.else_body)

    def visit_While(self, node):
        self.condition(node.condition)
        self.block(node.body)

    def visit_For(self, node):
        symbol = self.find_variable(node.var, node.line)

        if symbol.type != "int":
            raise SemanticError(node.line, f"flambar counter '{node.var}' must be int, but it is {symbol.type}")

        for expression, name in ((node.start, "start"), (node.end, "end")):
            value_type = self.expression(expression)

            if value_type != "int":
                raise SemanticError(node.line, f"range {name} must be int, but it is {value_type}")

        symbol.initialized = True
        self.block(node.body)

    def visit_FuncDecl(self, node):
        if self.function is not None or self.block_depth > 0:
            raise SemanticError(node.line, f"receita '{node.name}' must be declared at the top level of the program")

        param_types = [param.type_name for param in node.params]
        self.function = self.table.declare_function(node.name, param_types, node.return_type or "void", node.line)
        self.table.enter_function(node.name)

        for param in node.params:
            self.table.declare_parameter(param.name, param.type_name, param.line)

        for statement in node.body:
            self.visit(statement)

        if node.return_type is not None and not always_returns(node.body):
            raise SemanticError(node.line, f"receita '{node.name}' must end with 'comer' in every path")

        self.table.exit_function()
        self.function = None

    def visit_Return(self, node):
        if self.function is None:
            raise SemanticError(node.line, "'comer' can only be used inside a receita")

        name = self.function.name
        return_type = self.function.type

        if return_type == "void":
            if node.value is not None:
                raise SemanticError(node.line, f"receita '{name}' does not return a value, use 'comer;'")
            return

        if node.value is None:
            raise SemanticError(node.line, f"receita '{name}' must return a value of type {return_type}")

        value_type = self.expression(node.value)

        if not assignable(return_type, value_type):
            raise SemanticError(node.line, f"receita '{name}' returns {return_type} and cannot return a value of type {value_type}")

    def visit_CallStatement(self, node):
        self.check_call(node.call)

    def expression(self, node):
        if isinstance(node, IntLiteral):
            return "int"

        if isinstance(node, FloatLiteral):
            return "float"

        if isinstance(node, StrLiteral):
            return "str"

        if isinstance(node, CharLiteral):
            return "char"

        if isinstance(node, Group):
            return self.expression(node.expression)

        if isinstance(node, Variable):
            symbol = self.find_variable(node.name, node.line)

            if not symbol.initialized:
                raise SemanticError(node.line, f"variable '{node.name}' is used before receiving a value")

            return symbol.type

        if isinstance(node, UnaryOp):
            operand = self.expression(node.operand)

            if operand not in NUMERIC:
                raise SemanticError(node.line, f"unary '-' cannot be applied to {operand}")

            return operand

        if isinstance(node, BinaryOp):
            left = self.expression(node.left)
            right = self.expression(node.right)
            result = arithmetic_result(node.operator, left, right)

            if result is None:
                raise SemanticError(node.line, f"operator '{node.operator}' cannot be applied to {left} and {right}")

            return result

        if isinstance(node, Call):
            result = self.check_call(node)

            if result == "void":
                raise SemanticError(node.line, f"receita '{node.name}' does not return a value and cannot be used in an expression")

            return result

        raise TypeError(f"unknown expression: {node}")

    def condition(self, node):
        left = self.expression(node.left)
        right = self.expression(node.right)

        if not comparable(left, right):
            raise SemanticError(node.line, f"cannot compare {left} with {right} using '{node.operator}'")

    def check_call(self, call):
        symbol = self.table.lookup(call.name)

        if symbol is None:
            raise SemanticError(call.line, f"receita '{call.name}' was not declared")

        if symbol.kind != "receita":
            raise SemanticError(call.line, f"'{call.name}' is a variable, not a receita")

        if len(call.args) != len(symbol.params):
            raise SemanticError(call.line, f"receita '{call.name}' expects {len(symbol.params)} argument(s), but received {len(call.args)}")

        for position, (arg, param_type) in enumerate(zip(call.args, symbol.params), start=1):
            arg_type = self.expression(arg)

            if not assignable(param_type, arg_type):
                raise SemanticError(call.line, f"argument {position} of receita '{call.name}' must be {param_type}, but it is {arg_type}")

        return symbol.type

    def find_variable(self, name, line):
        symbol = self.table.lookup(name)

        if symbol is None:
            outer = self.table.lookup_global(name)

            if self.function is not None and outer is not None:
                raise SemanticError(line, f"variable '{name}' belongs to the main program and is not visible inside receita '{self.function.name}'")

            raise SemanticError(line, f"variable '{name}' was not declared")

        if symbol.kind == "receita":
            raise SemanticError(line, f"'{name}' is a receita, not a variable")

        return symbol

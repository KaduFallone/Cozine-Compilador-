from dataclasses import dataclass, fields, is_dataclass


@dataclass
class IntLiteral:
    value: int
    line: int

@dataclass
class FloatLiteral:
    value: str
    line: int

@dataclass
class StrLiteral:
    value: str
    line: int

@dataclass
class CharLiteral:
    value: str
    line: int

@dataclass
class Variable:
    name: str
    line: int

@dataclass
class Group:
    expression: object
    line: int

@dataclass
class UnaryOp:
    operator: str
    operand: object
    line: int

@dataclass
class BinaryOp:
    operator: str
    left: object
    right: object
    line: int

@dataclass
class Call:
    name: str
    args: list
    line: int

@dataclass
class Condition:
    operator: str
    left: object
    right: object
    line: int


@dataclass
class VarDecl:
    name: str
    type_name: str
    value: object
    line: int

@dataclass
class Assign:
    name: str
    value: object
    line: int

@dataclass
class Print:
    args: list
    line: int

@dataclass
class IfBranch:
    condition: Condition
    body: list
    line: int

@dataclass
class If:
    branches: list
    else_body: list
    line: int

@dataclass
class While:
    condition: Condition
    body: list
    line: int

@dataclass
class For:
    var: str
    start: object
    end: object
    body: list
    line: int

@dataclass
class Param:
    name: str
    type_name: str
    line: int

@dataclass
class FuncDecl:
    name: str
    params: list
    return_type: str
    body: list
    line: int

@dataclass
class Return:
    value: object
    line: int

@dataclass
class CallStatement:
    call: Call
    line: int

@dataclass
class Program:
    statements: list


def format_tree(node, indent=0):
    pad = "  " * indent

    if isinstance(node, list):
        return "".join(format_tree(item, indent) for item in node)

    attributes = []
    children = []

    for field in fields(node):
        value = getattr(node, field.name)

        if field.name == "line" or value is None:
            continue

        if is_dataclass(value) or isinstance(value, list):
            children.append((field.name, value))
        else:
            attributes.append(f"{field.name}={value!r}")

    text = f"{pad}{type(node).__name__} {' '.join(attributes)}".rstrip() + "\n"

    for name, value in children:
        text += f"{pad}  {name}:\n" + format_tree(value, indent + 2)

    return text

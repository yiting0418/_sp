from dataclasses import dataclass
from typing import Any, List, Optional

class Node: pass

@dataclass
class NumberLiteral(Node):
    value: float
    is_int: bool = True

@dataclass
class StringLiteral(Node):
    value: str

@dataclass
class BoolLiteral(Node):
    value: bool

@dataclass
class NullLiteral(Node):
    pass

@dataclass
class ArrayLiteral(Node):
    elements: List[Node]

@dataclass
class Identifier(Node):
    name: str

@dataclass
class BinaryOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class UnaryOp(Node):
    op: str
    operand: Node

@dataclass
class CompareOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class LogicalOp(Node):
    left: Node
    op: str
    right: Node

@dataclass
class NotOp(Node):
    operand: Node

@dataclass
class Index(Node):
    obj: Node
    idx: Node

@dataclass
class FuncCall(Node):
    callee: Node
    args: List[Node]

@dataclass
class Assign(Node):
    name: str
    value: Node

@dataclass
class Program(Node):
    body: List[Node]

@dataclass
class VarDecl(Node):
    name: str
    value: Node

@dataclass
class Block(Node):
    body: List[Node]

@dataclass
class IfStmt(Node):
    condition: Node
    then_block: Block
    else_block: Optional[Node] = None

@dataclass
class WhileStmt(Node):
    condition: Node
    body: Block

@dataclass
class ForStmt(Node):
    var: str
    start: Node
    end: Node
    step: Optional[Node]
    body: Block

@dataclass
class FuncDecl(Node):
    name: str
    params: List[str]
    body: Block

@dataclass
class ReturnStmt(Node):
    value: Optional[Node]

@dataclass
class BreakStmt(Node):
    pass

@dataclass
class ContinueStmt(Node):
    pass

@dataclass
class PrintStmt(Node):
    value: Node

@dataclass
class InputStmt(Node):
    var: str

import ast
import sys
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class ErrorCode(Enum):
    COPY_PASTE = '001', 'Copy-paste of code'
    MISSING_EARLY_QUIT = '002', 'Missing early quit'
    USING_EVAL = '003', 'Using eval'
    TRY_TOO_MUCH = '004', 'Too big "try" code block'
    REQUESTS_NO_STATUS_CHECK = '005', 'Not checking response status code'


@dataclass
class Error:
    PREFIX: ClassVar[str] = 'GRG'

    lineno: int
    col_offset: int
    code: ErrorCode
    snippet: str = ''

    @property
    def message(self) -> str:
        return f"{self.PREFIX}{self.code.value[0]} {self.code.value[1]}"


def get_root(node: ast.AST) -> ast.AST:
    while (parent := node.parent) is not None:  # type: ignore[attr-defined]
        node = parent

    return node


if sys.version_info < (3, 9):
    def unparse(node: ast.AST) -> str:
        """Fallback for ast.unparse in Python 3.8"""
        if isinstance(node, ast.Expr):
            return unparse(node.value)
        elif isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Call):
            func = unparse(node.func)
            args = [unparse(arg) for arg in node.args]
            return f"{func}({', '.join(args)})"
        elif isinstance(node, ast.Attribute):
            value = unparse(node.value)
            return f"{value}.{node.attr}"
        elif isinstance(node, ast.Assign):
            targets = [unparse(t) for t in node.targets]
            value = unparse(node.value)
            return f"{' = '.join(targets)} = {value}"
        elif isinstance(node, ast.Return):
            if node.value:
                return f"return {unparse(node.value)}"
            return "return"
        elif isinstance(node, ast.Raise):
            if node.exc:
                return f"raise {unparse(node.exc)}"
            return "raise"
        elif isinstance(node, ast.If):
            test = unparse(node.test)
            body = [unparse(stmt) for stmt in node.body]
            orelse = [unparse(stmt) for stmt in node.orelse]
            body_formatted = '\n    '.join(body)
            orelse_formatted = '\n    '.join(orelse)
            return "if {test}:\n    {body_formatted}\nelse:\n    {orelse_formatted}".format(
                test=test,
                body_formatted=body_formatted,
                orelse_formatted=orelse_formatted,
            )
        else:
            return str(node)
else:
    unparse = ast.unparse

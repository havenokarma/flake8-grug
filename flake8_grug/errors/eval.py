import ast
from typing import Optional

from . import Error, ErrorCode, unparse


def get_error_eval(node: ast.Call) -> Optional[Error]:
    assert isinstance(node, ast.Call)

    if isinstance(node.func, ast.Name) and node.func.id == 'eval':
        return Error(
            lineno=node.lineno,
            col_offset=node.col_offset,
            code=ErrorCode.USING_EVAL,
            snippet=unparse(node),
        )

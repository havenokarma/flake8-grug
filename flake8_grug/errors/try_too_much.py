import ast
from typing import Optional

from . import Error, ErrorCode, unparse


def get_error_try_too_much(node: ast.Call, max_lines: int = 3) -> Optional[Error]:
    assert isinstance(node, ast.Try)

    if len(node.body) > max_lines:
        return Error(
            lineno=node.lineno,
            col_offset=node.col_offset,
            code=ErrorCode.TRY_TOO_MUCH,
            snippet=unparse(node),
        )

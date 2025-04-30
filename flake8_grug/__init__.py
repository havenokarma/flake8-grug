import ast
import importlib
from dataclasses import dataclass
from typing import Any, ClassVar, Generator, Type, cast, List, Tuple

from .visitor import Visitor


@dataclass
class Plugin:
    name: ClassVar[str] = __name__
    version: ClassVar[str] = importlib.metadata.version(__name__)

    tree: ast.AST
    lines: List[str]

    def __post_init__(self) -> None:
        add_meta(self.tree)

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.lines = self.lines
        visitor.visit(self.tree)
        for error in visitor.errors:
            yield (error.lineno, error.col_offset, error.message, type(self))


# https://github.com/MartinThoma/flake8-simplify/blob/master/flake8_simplify/__init__.py
def add_meta(root: ast.AST, level: int = 0) -> None:
    if level == 0:
        root.parent = None  # type: ignore[attr-defined]

    previous_sibling = None
    for node in ast.iter_child_nodes(root):
        if level == 0:
            node.parent = root  # type: ignore[attr-defined]
        node.previous_sibling = previous_sibling  # type: ignore[attr-defined]
        node.next_sibling = None  # type: ignore[attr-defined]
        if previous_sibling:
            node.previous_sibling.next_sibling = node  # type: ignore[attr-defined]
        previous_sibling = node
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore[attr-defined]
        add_meta(node, level=level + 1)

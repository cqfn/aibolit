from javalang.ast import Node
from typing import List, Tuple
from aibolit.utils.ast import AST


class Lines:
    """
    Return the lines for some AST
    """
    def __init__(self, filename: str):
        self._filename = filename
        self._ast = AST(filename)
        self.value()

    def value(self) -> Tuple[Node, List[str]]:
        with open(self._filename, encoding=self._ast.encoding) as file:
            lines = file.readlines()

        return self._ast.value(), lines

from javalang.ast import Node
from javalang.tree import CompilationUnit
from typing import List, Tuple

from javalang.parse import parse

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class Lines:
    """
    Return the lines for some AST
    Deprecated: This class is used ony once by JavalangImproved
                and does not provide any complex functionality, so should be removed.
    """
    def __init__(self, filename: str):
        source_code = read_text_with_autodetected_encoding(filename)

        self._lines = source_code.splitlines(keepends=True)
        self._tree: CompilationUnit = parse(source_code)

    def value(self) -> Tuple[Node, List[str]]:
        return self._tree, self._lines

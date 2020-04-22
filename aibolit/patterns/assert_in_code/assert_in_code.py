from typing import List
from javalang.ast import Node
from javalang.tree import (
    CompilationUnit,
    AssertStatement,
    ClassDeclaration
)

from aibolit.types_decl import LineNumber
from aibolit.utils.ast import AST

_TEST_CLASS_SUFFIX = 'Test'


class AssertInCode(object):
    def value(self, filename: str) -> List[LineNumber]:
        tree: CompilationUnit = AST(filename).value()

        return self.__traverse_node(tree)

    def __traverse_node(self, tree: CompilationUnit) -> List[LineNumber]:
        lines: List[LineNumber] = list()

        for path, node in tree.filter(AssertStatement):
            lines.append(node.position.line)
        return lines


def _within_test_class(path) -> bool:
    class_declaration = next(filter(_is_class_declaration, path[::2]))

    return class_declaration.name.endswith(_TEST_CLASS_SUFFIX)


def _is_class_declaration(node: Node) -> bool:
    return isinstance(node, ClassDeclaration)

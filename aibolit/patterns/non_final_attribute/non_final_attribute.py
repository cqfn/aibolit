
from typing import List

import javalang
from javalang.tree import FieldDeclaration

from aibolit.types_decl import LineNumber


class NonFinalAttribute:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())
        return tree

    def value(self, filename: str) -> List[LineNumber]:
        tree = self.__file_to_ast(filename).filter(FieldDeclaration)

        return [node.position.line for path, node in tree if 'final' not in node.modifiers]

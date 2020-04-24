import os
from typing import Type
from javalang.parse import parse
from javalang.tree import CompilationUnit
from javalang import tree as tr


class AST:
    """
    Returns the AST for some java file
    """

    def __init__(self, filename: str):
        self._filename = filename

    def value(self) -> CompilationUnit:

        if os.path.splitext(self._filename)[1] != '.java':
            raise TypeError('Invalid file extension')

        with open(self._filename, encoding='utf-8') as file:
            return parse(file.read())

    @staticmethod
    def get_path_for_parent(path: tuple, ) -> tuple:
        contains = (
            tr.CompilationUnit,
            tr.ClassDeclaration,
            tr.MethodDeclaration,
            tr.LocalVariableDeclaration,
            tr.BlockStatement,
            tr.MethodInvocation,
            tr.ClassCreator,
            tr.TryStatement,
        )

        for index, i in enumerate(reversed(path)):
            if type(i) in contains:
                return path[index:]
        return ()

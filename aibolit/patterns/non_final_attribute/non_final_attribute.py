
from typing import List

from javalang.tree import FieldDeclaration, ClassDeclaration

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class NonFinalAttribute:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        ret = []
        for _, clazz in build_ast(filename).filter(ClassDeclaration):
            for _, field in clazz.filter(FieldDeclaration):
                if 'final' not in field.modifiers:
                    ret.append(field.position.line)
        return list(dict.fromkeys(ret))

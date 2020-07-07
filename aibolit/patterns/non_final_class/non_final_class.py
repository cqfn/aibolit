from typing import List

from aibolit.types_decl import LineNumber
from aibolit.ast_framework import ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        java_package = JavaPackage(filename)
        positions = []
        for java_class in java_package.java_classes.values():
            class_declaration_root = java_class.root
            modifiers_node, = java_class.get_first_n_children_with_type(class_declaration_root,
                                                                        ASTNodeType.COLLECTION, 1)
            if modifiers_node is None:
                continue
            modifiers = {java_class.get_attr(child, 'string') for child in
                         java_class.children_with_type(modifiers_node, ASTNodeType.STRING)}
            if len(modifiers & NonFinalClass._allowed_class_modifiers) == 0:
                positions.append(java_class.get_attr(class_declaration_root, 'line'))

        return positions

    _allowed_class_modifiers = {'final', 'abstract'}

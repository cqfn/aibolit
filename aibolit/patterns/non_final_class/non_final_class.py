from typing import List

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST.build_from_javalang(build_ast(filename))
        positions = []
        for class_declaration in tree.nodes_by_type(ASTNodeType.CLASS_DECLARATION):
            modifiers_node, = tree.get_first_n_children_with_type(class_declaration, ASTNodeType.COLLECTION, 1)
            if modifiers_node is None:
                continue
            modifiers = {tree.get_attr(child, 'string') for child in
                         tree.children_with_type(modifiers_node, ASTNodeType.STRING)}
            if len(modifiers & NonFinalClass._allowed_class_modifiers) == 0:
                positions.append(tree.get_attr(class_declaration, 'source_code_line'))

        return positions

    _allowed_class_modifiers = {'final', 'abstract'}

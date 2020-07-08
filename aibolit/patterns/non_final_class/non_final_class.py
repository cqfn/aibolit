from typing import List

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType


class NonFinalClass:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        tree = AST.build_from_javalang(build_ast(filename))
        positions = []
        for class_subgraph in tree.subtrees_with_root_type(ASTNodeType.CLASS_DECLARATION):
            class_declaration_root = class_subgraph[0]
            modifiers_node, = tree.get_first_n_children_with_type(class_declaration_root, ASTNodeType.COLLECTION, 1)
            if modifiers_node is None:
                continue
            modifiers = {tree.get_attr(child, 'string') for child in
                         tree.children_with_type(modifiers_node, ASTNodeType.STRING)}
            if len(modifiers & NonFinalClass._allowed_class_modifiers) == 0:
                positions.append(tree.get_attr(class_declaration_root, 'source_code_line'))

        return positions

    _allowed_class_modifiers = {'final', 'abstract'}

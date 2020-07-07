from typing import List

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType


class InstanceOf:
    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Traverse over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        tree = AST.build_from_javalang(build_ast(filename))
        lines: List[int] = []
        for node in tree.nodes_by_type(ASTNodeType.BINARY_OPERATION):
            if tree.get_binary_operation_name(node) == 'instanceof':
                lines.append(tree.get_line_number_from_children(node))

        for node in tree.nodes_by_type(ASTNodeType.METHOD_INVOCATION):
            method_name = tree.get_method_invocation_params(node).method_name
            if method_name == 'isInstance':
                lines.append(tree.get_attr(node, 'source_code_line'))

        return lines

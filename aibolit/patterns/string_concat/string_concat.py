from typing import Tuple, Dict, List
from typing import Tuple, Dict, List

from aibolit.types_decl import LineNumber
from aibolit.utils.utils import RemoveComments


class StringConcatFinder:

    def __init__(self):
        pass

    """
        @todo #131:30min NoComments implementation of Ast
         this __file_to_ast implementation differs from usual ones since it
         removes the comments from it. Implement a decorator to Ast which does
         it and replace it here. Don't forget the tests.
    """

    def __file_to_ast(self, filename: str) -> Tuple[str, Dict[str, int]]:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            text = file.read()
            lines_map = {line: i for i, line in enumerate(text.splitlines(), start=1)}
            res = RemoveComments.remove_comments(text)

        return res, lines_map

    # flake8: noqa: C901
    def value(self, filename: str) -> List[LineNumber]:
        import javalang
        lines = set()
        with open(filename, encoding='utf-8') as file:
            text = javalang.parse.parse(file.read())

        for _, node in text.filter(javalang.tree.BinaryOperation):
            if node.operator == '+':
                is_l_literal = isinstance(node.operandl, javalang.tree.Literal)
                is_r_literal = isinstance(node.operandr, javalang.tree.Literal)
                is_r_member = isinstance(node.operandr, javalang.tree.MemberReference)
                is_l_member = isinstance(node.operandl, javalang.tree.MemberReference)
                is_l_meth_inv = isinstance(node.operandl, javalang.tree.MethodInvocation)
                is_r_meth_inv = isinstance(node.operandr, javalang.tree.MethodInvocation)
                is_l_this = isinstance(node.operandl, javalang.tree.This)
                is_r_this = isinstance(node.operandr, javalang.tree.This)
                if is_l_literal and (is_r_member or is_r_meth_inv or is_r_this):
                    is_string_literal = '"' in node.operandl.value
                    if is_string_literal:
                        if node.operandl.position:
                            lines.add(node.operandl.position.line)
                        elif node.operandr.position:
                            lines.add(node.operandr.position.line)
                        elif hasattr(node.operandl, '_position'):
                            lines.add(node.operandl._position.line)
                        elif hasattr(node.operandr, '_position'):
                            lines.add(node.operandr._position.line)
                elif is_r_literal and (is_l_member or is_l_meth_inv or is_l_this):
                    is_string_literal = '"' in node.operandr.value
                    if is_string_literal:
                        if node.operandl.position:
                            lines.add(node.operandl.position.line)
                        elif node.operandr.position:
                            lines.add(node.operandr.position.line)
                        elif hasattr(node.operandr, '_position'):
                            lines.add(node.operandr._position.line)
                        elif hasattr(node.operandl, '_position'):
                            lines.add(node.operandl._position.line)

        return sorted(lines)

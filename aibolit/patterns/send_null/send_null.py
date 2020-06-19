import javalang
from typing import List

from aibolit.utils.ast_builder import build_ast


class SendNull:

    def __init__(self):
        pass

    def __find_position_recursively(self, node):
        if not hasattr(node, 'children'):
            return
        else:
            for i in node.children:
                if not isinstance(i, list):
                    if hasattr(i, '_position'):
                        if i.position:
                            return i._position.line
                        else:
                            for j in i.children:
                                position = self.__find_position_recursively(j)
                                if position:
                                    return position
                else:
                    for j in i:
                        position = self.__find_position_recursively(j)

        return position

    # flake8: noqa
    # after fix addition, errors are shown
    def value(self, filename: str) -> List[int]:

        lst: List[int] = []
        tree = build_ast(filename)

        invocation_tree = tree.filter(javalang.tree.Invocation)
        arg_list = [x for _, x in invocation_tree]

        for argument in arg_list:
            ternary_list = argument.filter(javalang.tree.TernaryExpression)
            for _, expr in ternary_list:
                if isinstance(expr.if_false, javalang.tree.Literal) and expr.if_false.value == 'null':
                    if hasattr(argument, '_position'):
                        lst.append(argument._position.line)
                    else:
                        position = self.__find_position_recursively(expr)
                        lst.append(position)
                if isinstance(expr.if_true, javalang.tree.Literal) and expr.if_true.value == 'null':
                    if hasattr(argument, '_position'):
                        lst.append(argument._position.line)
                    else:
                        position = self.__find_position_recursively(expr)
                        lst.append(position)

        for _, node in tree:
            try:
                for argument in node.arguments:
                    if isinstance(argument, javalang.tree.Literal) and argument.value == "null" and \
                            argument._position.line not in lst:
                        lst.append(argument._position.line)
            except (AttributeError, TypeError):
                pass
        lst = sorted(lst)
        return lst

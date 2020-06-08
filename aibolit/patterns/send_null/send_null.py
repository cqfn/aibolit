import javalang
from typing import List

from aibolit.utils.ast_builder import build_ast


class SendNull:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        lst: List[int] = []
        tree = build_ast(filename)

        invocation_tree = tree.filter(javalang.tree.Invocation)
        arg_list = [x for _, x in invocation_tree]

        for argument in arg_list:
            ternary_list = argument.filter(javalang.tree.TernaryExpression)
            for _, expr in ternary_list:
                if isinstance(expr.if_false, javalang.tree.Literal) and expr.if_false.value == 'null':
                    lst.append(argument._position.line)
                if isinstance(expr.if_true, javalang.tree.Literal) and expr.if_true.value == 'null':
                    lst.append(argument._position.line)

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

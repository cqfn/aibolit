import javalang
from aibolit.utils.ast import AST
from typing import List


class SendNull:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        lst: List[int] = []
        tree = AST(filename).value()
        invocation_tree = tree.filter(javalang.tree.Invocation)

        for path, node in invocation_tree:
            for argument in node.arguments:
                if isinstance(argument, javalang.tree.Literal) and argument.value == "null" and \
                        argument._position.line not in lst:
                    lst.append(argument._position.line)
        lst = sorted(lst)
        return lst

import javalang
from aibolit.utils.ast import AST


class SendNull:

    def __init__(self):
        pass

    def value(self, filename: str):
        lst = []
        tree = AST(filename).value()
        method_tree = tree.filter(javalang.tree.MethodInvocation)
        constructor_tree = tree.filter(javalang.tree.ExplicitConstructorInvocation)

        for path, node in constructor_tree:
            for argument in node.arguments:
                if type(argument) == javalang.tree.Literal and argument.value == "null" and \
                        argument._position.line not in lst:
                    lst.append(argument._position.line)

        for path, node in method_tree:
            for argument in node.arguments:
                if type(argument) == javalang.tree.Literal and argument.value == "null" and \
                        argument._position.line not in lst:
                    lst.append(argument._position.line)
        return lst

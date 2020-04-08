from os import terminal_size

import javalang
from aibolit.utils.ast import AST


class JoinedValidation:
    '''
    Returns lines with if statement which has also has a single throws inside and its check contains more than one
    condition joined with OR.
    '''
    def __init__(self):
        pass

    def value(self, filename: str):
        return [
            type(node)
            for _, node in AST(filename).value().filter(javalang.tree.IfStatement)
            if node.condition.operator == '||' and type(node.then_statement.statements[0]) == javalang.tree.ThrowStatement
        ]



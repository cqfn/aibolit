import javalang
import re
from aibolit.utils.ast import AST


class VarSiblings:
    def __init__(self):
        pass

    def value(self, filename: str):
        numbers = []
        for _, node in AST(filename).value().filter(javalang.tree.LocalVariableDeclaration):
            composed = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node.declarators[0].name)
            if len(composed) > 1:
                for _, inner in AST(filename).value().filter(javalang.tree.LocalVariableDeclaration):
                    if node != inner:
                        if inner.declarators[0].name.startswith(composed[0]):
                            numbers.append(node.position.line)
                            break
        return numbers

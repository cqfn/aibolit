import javalang
import re
import itertools

from aibolit.utils.ast_builder import build_ast


class VarSiblings:
    def __init__(self):
        pass

    def value(self, filename: str):
        numbers = []
        for first, second in itertools.product(
            [node
                for _, node in build_ast(filename).filter(javalang.tree.LocalVariableDeclaration)
                if len(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node.declarators[0].name)) > 1
                and len(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', node.declarators[0].name)[0]) > 3],  # noqa: W503
                repeat=2
        ):
            if first != second:
                if second.declarators[0].name.startswith(
                    re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', first.declarators[0].name)[0]
                ):
                    numbers.append(first.position.line)
        return numbers

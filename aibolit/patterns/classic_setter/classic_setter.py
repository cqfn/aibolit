from typing import List

import javalang

from aibolit.types_decl import LineNumber
from aibolit.utils.ast_builder import build_ast


class ClassicSetter:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        lst: List[LineNumber] = []
        tree = build_ast(filename).filter(javalang.tree.MethodDeclaration)
        for _, node in tree:
            if (node.return_type is None) and ('set' in node.name[:3]):
                if (isinstance(node.body, list)) and len(node.body) < 2:
                    for statement in node.body:
                        if isinstance(statement, javalang.tree.StatementExpression):
                            if isinstance(statement.expression, javalang.tree.Assignment):
                                expression = statement.expression.expressionl
                                if isinstance(expression, javalang.tree.This):
                                    if statement.expression.type == '=':
                                        if expression.selectors[0].member.lower() == node.name.lower()[3:]:
                                            lst.append(node._position.line)
                                    else:
                                        break
                                else:
                                    break
                            else:
                                break
        return lst

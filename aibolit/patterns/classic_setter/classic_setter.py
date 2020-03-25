import javalang


class ClassicSetter:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())
        return tree

    def value(self, filename: str):
        lst = []
        tree = self.__file_to_ast(filename).filter(javalang.tree.MethodDeclaration)
        for path, node in tree:
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

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
        expr = javalang.tree.StatementExpression
        tree = self.__file_to_ast(filename).filter(javalang.tree.MethodDeclaration)
        for path, node in tree:
            assing_statement = 0
            if node.return_type is None and ('set' in node.name[:3]) and isinstance(node.body, list):
                for stmn in node.body:
                    if isinstance(stmn, expr):
                        if isinstance(stmn.expression, javalang.tree.Assignment):
                            if isinstance(stmn.expression.expressionl, javalang.tree.This):
                                selector_name = stmn.expression.expressionl.selectors[0].member.lower()
                                if stmn.expression.type == '=' and (selector_name == node.name.lower()[3:]):
                                    assing_statement += 1
                        else:
                            break
                    elif isinstance(stmn, javalang.tree.AssertStatement):
                        continue
                    else:
                        break
                if assing_statement == 1:
                    lst.append(node._position.line)
        return lst

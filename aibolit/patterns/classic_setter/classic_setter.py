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
            if (node.return_type == None) and ('set' in node.name[:3]):
                if (node.return_type == None) and (isinstance(node.body, list)):
                    for stmnt in node.body:
                        if isinstance(stmnt, expr):
                            if isinstance(stmnt.expression, javalang.tree.Assignment):
                                if isinstance(stmnt.expression.expressionl, javalang.tree.This):
                                    if stmnt.expression.type == '=':
                                        if stmnt.expression.expressionl.selectors[0].member.lower() == node.name.lower()[3:]:
                                            assing_statement += 1
                            else:
                                break
                        elif isinstance(stmnt, javalang.tree.AssertStatement):
                            continue
                        else:
                            break
                    if assing_statement == 1:
                        #print(node.body)
                        lst.append(node._position.line)
        return lst

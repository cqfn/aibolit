import javalang


class ClassicGetter:

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
        lst = list()
        tree = self.__file_to_ast(filename).filter(javalang.tree.MethodDeclaration)
        
        for path, node in tree:
        
            #if (node.return_type == None) and ('get' in node.name[:3]) and (isinstance(node.body, list)) and len(node.body) < 2 :    
            if  ('get' in node.name[:3]) and (isinstance(node.body, list)) and len(node.body) < 2 :    
                if isinstance(node.body[0], javalang.tree.ReturnStatement):
                    for statement in node.body:
                        #if statement.expression.expressionl.selectors[0].member.lower() == node.name.lower()[3:]:
                        #print(name, node._position.line, node.name, type((node.body[0])), (statement[0]))
                        if isinstance(statement, javalang.tree.ReturnStatement):
                            if isinstance(statement.children[1], javalang.tree.MemberReference):
                                if node.name.lower()[3:] == statement.children[1].member.lower():
                                    lst.append(node._position.line)
                                    
                                    #print(name, node._position.line, node.name, (statement.children[1].member))
        return lst
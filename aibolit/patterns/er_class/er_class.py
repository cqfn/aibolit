import javalang


class ErClass:

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
        classes = ('manager',
                   'controller',
                   'router',
                   'dispatcher',
                   'printer',
                   'writer',
                   'reader',
                   'parser',
                   'generator',
                   'renderer',
                   'listener',
                   'producer',
                   'holder',
                   'interceptor')
        tree = self.__file_to_ast(filename).filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if [n for n in classes if n in node.name.lower()] != []]

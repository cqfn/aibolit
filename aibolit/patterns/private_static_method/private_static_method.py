import javalang


class PrivateStaticMethod:

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
        tree = self.__file_to_ast(filename).filter(javalang.tree.MethodDeclaration)
        return [node for path, node in tree if 'private' in node.modifiers and 'static' in node.modifiers]

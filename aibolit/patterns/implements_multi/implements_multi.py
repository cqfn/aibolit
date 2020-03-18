import re
import javalang

class ImplementsMultiFinder:

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
        tree = self.__file_to_ast(filename)
        newlist = [node for _ , node in tree.filter(javalang.tree.ClassDeclaration) if node.implements]
        out = list()
        for node in newlist:
            if len(node.implements) > 1:
                out.append(node._position.line)
        return out


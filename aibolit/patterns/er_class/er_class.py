import javalang
from aibolit.utils.ast import AST


class ErClass:

    def __init__(self):
        pass

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
        tree = AST(filename).value().filter(javalang.tree.ClassDeclaration)
        return [node._position.line for _, node in tree if [n for n in classes if n in node.name.lower()] != []]

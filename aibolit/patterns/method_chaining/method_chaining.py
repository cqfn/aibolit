import javalang

from aibolit.utils.utils import remove_comments


class MethodChainFinder:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = javalang.parse.parse(remove_comments(file.read()))
        return res

    def value(self, filename: str):
        tree = self.__file_to_ast(filename)
        chain_list_methods = []
        for path, node in tree.filter(javalang.tree.StatementExpression):
            methods_invoked = []
            if isinstance(node.expression, javalang.tree.MethodInvocation):
                children = node.children
                for item in children:
                    if item:
                        if isinstance(item, javalang.tree.MethodInvocation):
                            inner_children = item.children
                            for j in inner_children:
                                if isinstance(j, list) or isinstance(j, tuple):
                                    for method in j:
                                        if isinstance(method, javalang.tree.MethodInvocation):
                                            methods_invoked.append(method.member)
            if methods_invoked:
                chain_list_methods.append(methods_invoked)

        return chain_list_methods

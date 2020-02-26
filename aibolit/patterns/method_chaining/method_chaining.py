import javalang

from aibolit.utils.utils import remove_comments
import uuid
from collections import defaultdict


class MethodChainFind:

    def __init__(self):
        pass

    def traverse_node(self, node, dict_with_chains, uuid_method):
        if not node:
            return dict_with_chains

        for item in node.children:
            if item and (isinstance(item, tuple) or isinstance(item, list)):
                for j in item:
                    if isinstance(j, javalang.tree.MethodInvocation):
                        dict_with_chains[uuid_method].append(j.member)
                        self.traverse_node(j, dict_with_chains, uuid_method)

                    elif isinstance(j, javalang.tree.MethodDeclaration):
                        self.traverse_node(j, dict_with_chains, uuid.uuid1())

                    elif isinstance(j, javalang.tree.StatementExpression):
                        self.traverse_node(j, dict_with_chains, uuid_method)

                    elif isinstance(j, javalang.tree.This) or isinstance(j, javalang.tree.ClassCreator):
                        self.traverse_node(j, dict_with_chains, uuid.uuid1())
            elif isinstance(item, javalang.tree.ClassCreator):
                self.traverse_node(item, dict_with_chains, uuid_method)

        return dict_with_chains

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = javalang.parse.parse(remove_comments(file.read()))
        return res

    # flake8: noqa: C901
    def value(self, filename: str):
        """
        Travers over AST tree finds method chaining. It is searched in a statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, ['func1', 'fun2']], [23, ['run', 'start']]]
        """
        tree = self.__file_to_ast(filename)
        chain_lst = defaultdict(list)
        for path, node in tree.filter(javalang.tree.StatementExpression):
            if isinstance(node.expression, javalang.tree.MethodInvocation):
                children = node.children
                if isinstance(children[1], javalang.tree.MethodInvocation):
                    uuid_first_method = str(uuid.uuid1())
                    chain_lst[uuid_first_method].append(children[1].member)
                    self.traverse_node(children[1], chain_lst, uuid_first_method)

        filtered_dict = list(filter(lambda elem: len(elem) > 1, chain_lst.values()))
        return filtered_dict

import javalang

import uuid
from collections import defaultdict
from aibolit.utils.ast import AST


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
                        if not j.qualifier and j.qualifier != '':
                            # it means that there is method chaining
                            dict_with_chains[uuid_method].append([j.position.line, j.member])
                            self.traverse_node(j, dict_with_chains, uuid_method)
                        else:
                            # it means that we have method invocation without chaining like
                            # result.add(field.getName(), column.columnName(), field.getType());
                            new_uuid = uuid.uuid1()
                            dict_with_chains[new_uuid].append([j.position.line, j.member])
                            self.traverse_node(j, dict_with_chains, new_uuid)

                    elif isinstance(j, javalang.tree.MethodDeclaration):
                        self.traverse_node(j, dict_with_chains, str(uuid.uuid1()))

                    elif isinstance(j, javalang.tree.StatementExpression):
                        self.traverse_node(j, dict_with_chains, uuid_method)

                    elif isinstance(j, javalang.tree.This) or isinstance(j, javalang.tree.ClassCreator):
                        self.traverse_node(j, dict_with_chains, str(uuid.uuid1()))
            elif isinstance(item, javalang.tree.ClassCreator):
                self.traverse_node(item, dict_with_chains, uuid_method)

        return dict_with_chains


    # flake8: noqa: C901
    def value(self, filename: str):
        """
        Travers over AST tree finds method chaining. It is searched in a statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, 'func1'], [10, 'fun2']], [[23, 'run'], [23, 'start']]]
        """
        tree = AST(filename).value()
        chain_lst = defaultdict(list)
        for path, node in tree.filter(javalang.tree.StatementExpression):
            if isinstance(node.expression, javalang.tree.MethodInvocation):
                children = node.children
                if isinstance(children[1], javalang.tree.MethodInvocation):
                    uuid_first_method = str(uuid.uuid1())
                    chain_lst[uuid_first_method].append([
                        children[1].position.line, children[1].member])
                    self.traverse_node(children[1], chain_lst, uuid_first_method)

        filtered_dict = list(filter(lambda elem: len(elem) > 1, chain_lst.values()))
        return [item[0][0] for item in filtered_dict]

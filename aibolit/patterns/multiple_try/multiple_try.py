import javalang
from typing import List
import uuid
from collections import defaultdict
import hashlib
import itertools
from aibolit.utils.ast import AST
from javalang.tree import FormalParameter

class MultipleTry:

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
        Travers over AST tree and fins function with nested/sequential try statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, 'func1'], [10, 'fun2']], [[23, 'run'], [23, 'start']]]
        """

        tree = AST(filename).value()
        res = defaultdict(list)
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                formal_params = [
                    (x.type.name + ' ' + x.name)  
                    for x in method_node.parameters 
                    if isinstance(x, FormalParameter)
                ]
                func_name = '{f}({params})'.format(
                    f=method_node.name,
                    params=','.join(formal_params)
                ).encode('utf-8')
                m = hashlib.md5()
                m.update(func_name)
                res[m.hexdigest()].append(method_node.position.line)

        return list(set(itertools.chain.from_iterable([y for x, y in res.items() if len(y) > 1])))
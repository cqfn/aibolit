import javalang

from collections import defaultdict
import hashlib
import itertools


class MultipleWhile:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = javalang.parse.parse(file.read())
        return res

    def value(self, filename: str):
        """
        Travers over AST tree and finds function with sequential while statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, 'func1'], [10, 'fun2']], [[23, 'run'], [23, 'start']]]
        """

        tree = self.__file_to_ast(filename)
        res = defaultdict(list)
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            for _, while_node in method_node.filter(javalang.tree.WhileStatement):
                func_name = '{f}({params})'.format(
                    f=method_node.name,
                    params=','.join([(x.type.name + ' ' + x.name) for x in method_node.parameters])
                ).encode('utf-8')
                m = hashlib.md5()
                m.update(func_name)
                res[m.hexdigest()].append(method_node.position.line)

        return list(set(itertools.chain.from_iterable([y for x, y in res.items() if len(y) > 1])))

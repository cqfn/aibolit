import javalang

from collections import defaultdict
from aibolit.utils.ast import AST
import hashlib
import itertools
from javalang.tree import FormalParameter


class MultipleWhile:

    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Travers over AST tree and finds function with sequential while statement
        :param filename:
        :return:
        List of tuples with LineNumber and List of methods names, e.g.
        [[10, 'func1'], [10, 'fun2']], [[23, 'run'], [23, 'start']]]
        """

        res = defaultdict(list)
        for _, method_node in AST(filename).value().filter(javalang.tree.MethodDeclaration):
            for _, while_node in method_node.filter(javalang.tree.WhileStatement):
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

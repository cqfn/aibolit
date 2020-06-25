from aibolit.utils.ast_builder import build_ast
from javalang.tree import ClassCreator, ClassDeclaration, MethodInvocation
from typing import List


class FanOut:
    '''
    Fan Out metric is defined as the number of other classes referenced by a class.
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        fan_outs = []
        tree = build_ast(filename)
        for _, class_body in tree.filter(ClassDeclaration):
            each_fanout = 0
            for _, invoked_class in class_body.filter(ClassCreator):
                each_fanout += 1

            # to count calling external class's methods
            for _, external_method in class_body.filter(MethodInvocation):
                if external_method.qualifier not in ['', class_body.name]:
                    each_fanout += 1

            fan_outs.append(each_fanout)
        return fan_outs

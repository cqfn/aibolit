from aibolit.utils.ast_builder import build_ast
from javalang.tree import MethodDeclaration, ClassDeclaration, VariableDeclarator
from typing import List


class NumMethodsAndVars:
    '''
    This class count number of methods and variables in class
    input: ast
    output: list(number of methods, number of variables)
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> List:
        tree = build_ast(filename)
        count_methods = 0
        count_variables = 0
        for _, class_body in tree.filter(ClassDeclaration):
            for each_object in class_body.body:
                if isinstance(each_object, MethodDeclaration):
                    count_methods += 1
        count_variables = sum([1 for _, var_body in tree.filter(VariableDeclarator)])

        return [count_methods, count_variables]

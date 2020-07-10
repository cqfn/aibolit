from aibolit.ast_framework.ast import ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage
from typing import List


class SuperMethod:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        """
        Iterates over functions and finds super.func() calls.
        Javalang doesn't have code line for super.func() call,
        that's why we can only count the first match of a call inside some function.
        It has MULTIPLE MATCHES if we call super.func() inside a ANONYMOUS CLASS.
        :param filename:
        :return: Lines of code
        """
        results = []
        tree = JavaPackage(filename)
        for ast_method in tree.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            for statement in ast_method.get_nodes(ASTNodeType.STATEMENT_EXPRESSION):
                code_line = ast_method.get_attr(statement, 'line')
                all_super_methods = ast_method.children_with_type(statement, ASTNodeType.SUPER_METHOD_INVOCATION)
                if len(list(all_super_methods)):
                    results.append(code_line)
        return results

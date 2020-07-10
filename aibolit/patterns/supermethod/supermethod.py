from aibolit.ast_framework.ast import AST, ASTNodeType
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
        for method_decl_node in tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION):
            ast = AST(tree.tree.subgraph(method_decl_node), method_decl_node[0])
            for i in ast.nodes_by_type(ASTNodeType.STATEMENT_EXPRESSION):
                code_line = ast.get_attr(i, 'source_code_line')
                j = list(ast.children_with_type(i, ASTNodeType.SUPER_METHOD_INVOCATION))
                if len(j):
                    results.append(code_line)
        return results

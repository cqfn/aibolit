from typing import List
from aibolit.types_decl import LineNumber
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.ast_framework.java_package import JavaPackage


class ClassicSetter:

    def __init__(self):
        pass

    def check_nodes(self, ast: AST, body_nodes: List) -> bool:
        '''
        In this function we check whether
        nodes in the function are agree with
        the definition of classic setter or not.
        Classic setter should consist of only several
        assert_statement and THIS statement.
        This statement is not-directed child of
        STATEMENT_EXPRESSION.
        '''
        suitable_nodes = [
            ASTNodeType.ASSERT_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
        ]
        for node in body_nodes:
            if ast.get_type(node.node_index) not in suitable_nodes:
                return False
        return True

    def value(self, filename: str) -> List[LineNumber]:
        lst: List[LineNumber] = []
        ast = JavaPackage(filename)
        method_decls = list(ast.get_nodes(ASTNodeType.METHOD_DECLARATION))
        for node in method_decls:
            method_name = ast.get_attr(node, 'name')
            body_nodes = ast.get_attr(node, 'body')
            if ast.get_attr(node, 'return_type') is None:
                if method_name.startswith('set') and self.check_nodes(ast, body_nodes):
                    for child_this in ast.get_nodes(ASTNodeType.THIS):
                        child_membref = ast.get_attr(child_this, 'selectors')
                        if len(child_membref):
                            referenced_name = ast.get_attr(child_membref[0].node_index, 'member')
                            source_line = ast.get_attr(node, 'line')
                            if method_name.lower()[3:] == referenced_name.lower() and source_line not in lst:
                                lst.append(source_line)
        return lst

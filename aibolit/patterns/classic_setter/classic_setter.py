from typing import Set, List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast


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
        suitable_nodes: List[ASTNodeType] = [
            ASTNodeType.ASSERT_STATEMENT,
            ASTNodeType.STATEMENT_EXPRESSION,
        ]
        for node in body_nodes:
            if node.node_type not in suitable_nodes:
                return False
        return True

    def value(self, filename: str) -> List[int]:
        lst: Set[int] = set()
        ast = AST.build_from_javalang(build_ast(filename))
        method_decls = list(ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION))
        for node in method_decls:
            method_name = node.name
            if node.return_type is None:
                if method_name.startswith('set') and self.check_nodes(ast, node.body):
                    for child_this in ast.get_proxy_nodes(ASTNodeType.THIS):
                        child_membref = child_this.selectors
                        if len(child_membref):
                            referenced_name = child_membref[0].member
                            source_line = node.line
                            if method_name.lower()[3:] == referenced_name.lower():
                                lst.add(source_line)
        return sorted(list(lst))

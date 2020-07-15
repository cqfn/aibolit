from typing import Set, List
from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework.ast_node import ASTNode


class ClassicSetter:
    '''
    The method's name starts with set, then goes
    the name of the attribute. There are attributes
    assigning in the method. Also, asserts are ignored.
    '''
    suitable_nodes: List[ASTNodeType] = [
        ASTNodeType.ASSERT_STATEMENT,
        ASTNodeType.STATEMENT_EXPRESSION,
    ]

    def _process_this_statements(self, ast: AST, node: ASTNode):
        lines: Set[int] = set()
        for child_this in ast.get_proxy_nodes(ASTNodeType.THIS):
            child_membref = child_this.selectors
            if len(child_membref):
                mem_referenced_name = child_membref[0].member
                source_line = node.line
                if node.name.lower()[3:] == mem_referenced_name.lower():
                    lines.add(source_line)
        return lines

    def _check_nodes(self, ast: AST, check_setter_body: List[ASTNode]) -> bool:
        '''
        In this function we check whether
        nodes in the function are agree with
        the definition of classic setter or not.
        Classic setter should consist of only several
        assert_statement and THIS statement.
        This statement is not-directed child of
        STATEMENT_EXPRESSION.
        '''
        for node in check_setter_body:
            if node.node_type not in self.suitable_nodes:
                return False
        return True

    def value(self, filename: str) -> List[int]:
        lines: Set[int] = set()
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if node.return_type is None and \
                    method_name.startswith('set') and self._check_nodes(ast, node.body):
                lines = lines.union(self._process_this_statements(ast, node))
        return sorted(list(lines))

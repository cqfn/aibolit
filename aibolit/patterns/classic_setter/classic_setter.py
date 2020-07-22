from typing import List
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

    def _check_this_statements(self, ast: AST, node: ASTNode) -> bool:
        for child_this in ast.get_subtree(node).get_proxy_nodes(ASTNodeType.THIS):
            child_membref = child_this.selectors
            if len(child_membref):
                mem_referenced_name = child_membref[0].member
                if node.name.lower() == 'set' + mem_referenced_name.lower():
                    return True
        return False

    def _check_body_nodes(self, check_setter_body: List[ASTNode]) -> bool:
        '''
        Check whether nodes are agree with the following types
        (in self.suitable_nodes) or not.
        '''
        for node in check_setter_body:
            if node.node_type not in self.suitable_nodes:
                return False
        return True

    def value(self, filename: str) -> List[int]:
        lines: List[int] = []
        ast = AST.build_from_javalang(build_ast(filename))
        for node in ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            method_name = node.name
            if node.return_type is None and method_name.startswith('set') and \
               self._check_body_nodes(node.body) and self._check_this_statements(ast, node):
                lines.append(node.line)
        return sorted(lines)

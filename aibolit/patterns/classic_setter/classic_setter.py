from typing import List
import re
from aibolit.types_decl import LineNumber
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage

extra_childs = [
    ASTNodeType.STRING,
    ASTNodeType.COLLECTION,
    ASTNodeType.ANNOTATION,
]


class ClassicSetter:

    def __init__(self):
        pass

    def _check_extra_child(self, ast: AST, node: int) -> List[int]:
        body_nodes = []
        for i in ast.tree.succ[node]:
            if ast.get_type(i) not in extra_childs:
                body_nodes.append(i)
        return body_nodes

    def _get_node_name(self, ast: AST, node: int) -> str:
        extracted_name = None
        names = ast.children_with_type(node, ASTNodeType.STRING)
        for each_string in names:
            method_name = ast.get_attr(each_string, 'string')
            if not method_name.startswith('/') and re.search(r'[^\W\d]', method_name) is not None:
                extracted_name = method_name
                return extracted_name
        return ''

    def value(self, filename: str) -> List[LineNumber]:
        lst: List[LineNumber] = []
        ast = JavaPackage(filename)
        method_decls = list(ast.nodes_by_type(ASTNodeType.METHOD_DECLARATION))
        for node in method_decls:
            method_name = self._get_node_name(ast, node)
            body_nodes = self._check_extra_child(ast, node)

            return_type = list(ast.children_with_type(node, ASTNodeType.BASIC_TYPE))
            if len(return_type) == 0 and ('set' in method_name[:3]) and len(body_nodes) < 3:
                childs_stat_expr = ast.children_with_type(node, ASTNodeType.STATEMENT_EXPRESSION)
                for expr_child in childs_stat_expr:
                    childs_assignment = ast.children_with_type(expr_child, ASTNodeType.ASSIGNMENT)
                    for child_assign in childs_assignment:
                        childs_this = list(ast.children_with_type(child_assign, ASTNodeType.THIS))
                        if len(childs_this):
                            for type_expr in ast.children_with_type(child_assign, ASTNodeType.STRING):
                                if ast.get_attr(type_expr, 'string') == '=':
                                    child_membref = ast.children_with_type(childs_this[0], ASTNodeType.MEMBER_REFERENCE)
                                    for each_ref in child_membref:
                                        if method_name.lower()[3:] == self._get_node_name(ast, each_ref).lower():
                                            lst.append(ast.get_attr(node, 'source_code_line'))
                                else:
                                    break
                        else:
                            break
        return lst

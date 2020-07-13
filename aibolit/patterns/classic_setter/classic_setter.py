from typing import List
from aibolit.types_decl import LineNumber
from aibolit.ast_framework import ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage


class ClassicSetter:

    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        lst: Set[LineNumber] = []
        ast = JavaPackage(filename)
        method_decls = list(ast.get_nodes(ASTNodeType.METHOD_DECLARATION))
        for node in method_decls:
            method_name = ast.get_attr(node, 'name')
            body_nodes = ast.get_attr(node, 'body')
            if (ast.get_attr(node, 'return_type') is None) and method_name.startswith('set') and len(body_nodes) < 2:
                for expr_child in ast.get_attr(node, 'body'):
                    for child_this in ast.get_nodes(ASTNodeType.THIS):
                        child_membref = ast.get_attr(child_this, 'selectors')
                        if len(child_membref):
                            referenced_name = ast.get_attr(child_membref[0].node_index, 'member')
                            source_line = ast.get_attr(node, 'line')
                            if method_name.lower()[3:] == referenced_name.lower() and source_line not in lst:
                                lst.append(source_line)
        return lst

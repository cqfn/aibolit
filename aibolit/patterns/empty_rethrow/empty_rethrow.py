from aibolit.ast_framework import ASTNodeType, AST
from aibolit.utils.ast_builder import build_ast
from typing import List, Set


class EmptyRethrow:

    def __init__(self):
        pass

    def value(self, filename) -> List[int]:
        total_code_lines: Set = set()
        ast = AST.build_from_javalang(build_ast(filename))
        method_decls = list(ast.get_proxy_nodes(ASTNodeType.METHOD_DECLARATION))
        for method_node in method_decls:
            for try_node in list(ast.get_proxy_nodes(ASTNodeType.TRY_STATEMENT)):
                for throw_node in list(ast.get_proxy_nodes(ASTNodeType.THROW_STATEMENT)):
                    field_catche = try_node.catches
                    if field_catche:
                        catch_classes = [x.parameter.name for x in field_catche]
                        mem_ref = list(throw_node.children)[0]
                        if mem_ref.node_type == ASTNodeType.CLASS_CREATOR:
                            continue

                        else:
                            if hasattr(mem_ref, 'member') and mem_ref.member in catch_classes:
                                total_code_lines.add(mem_ref.line)
        return sorted(total_code_lines)

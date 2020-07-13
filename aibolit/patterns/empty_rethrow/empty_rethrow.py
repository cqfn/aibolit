from aibolit.ast_framework import ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage
from typing import List, Set


class EmptyRethrow:

    def __init__(self):
        pass

    def value(self, filename) -> List[int]:
        total_code_lines: Set = set()
        ast = JavaPackage(filename)
        method_decls = list(ast.get_nodes(ASTNodeType.METHOD_DECLARATION))
        for method_node in method_decls:
            for try_node in list(ast.get_nodes(ASTNodeType.TRY_STATEMENT)):
                for throw_node in list(ast.get_nodes(ASTNodeType.THROW_STATEMENT)):
                    field_catche = ast.get_attr(try_node, 'catches')
                    if field_catche:
                        catch_classes = [ast.get_attr(ast.get_attr(x[0], 'parameter')[0], 'name') for x in field_catche]
                        mem_ref = list(ast.tree.succ[throw_node].keys())[0]
                        if ast.get_type(mem_ref) == ASTNodeType.CLASS_CREATOR:
                            continue
                        else:
                            member = ast.get_attr(mem_ref, 'member')
                            if member is not None and member in catch_classes:
                                total_code_lines.add(ast.get_attr(mem_ref, 'line'))
        return sorted(total_code_lines)

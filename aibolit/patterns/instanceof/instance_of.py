from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class InstanceOf:
    def __init__(self):
        pass

    def value(self, filename: str):
        """
        Traverse over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        tree = AST(build_ast(filename))
        lines = tree.check_binary_operation('instanceof', [])

        nodes = tree.nodes_by_type(ASTNodeType.METHOD_INVOCATION)
        for node in nodes:
            cur_line = tree.get_attr(node, 'source_code_line')
            str_attrs = list(tree.children_with_type(node, ASTNodeType.STRING))
            if tree.tree.nodes[str_attrs[0]]['string'] == 'isInstance':
                lines.append(cur_line)

        return lines

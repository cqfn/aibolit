from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType


class InstanceOf:
    def __init__(self):
        pass

    def get_line_number(self, node, tree):
        cur_line = 0
        cur_node = tree.tree.nodes[node]
        if 'source_code_line' in cur_node:
            cur_line = cur_node['source_code_line']
            return cur_line
        for child in tree.tree.succ[node]:
            cur_node = tree.tree.nodes[child]
            if 'source_code_line' in cur_node:
                cur_line = cur_node['source_code_line']
                break
        return cur_line

    def value(self, filename: str):
        """
        Traverse over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        tree = AST(build_ast(filename))
        lines = []

        nodes = tree.nodes_by_type(ASTNodeType.BINARY_OPERATION)
        for node in nodes:
            cur_line = self.get_line_number(node, tree)
            children = tree.children_with_type(node, ASTNodeType.STRING)
            for child in children:
                cur_node = tree.tree.nodes[child]
                if cur_node['type'] == ASTNodeType.STRING and cur_node['string'] == 'instanceof':
                    lines.append(cur_line)

        nodes = tree.nodes_by_type(ASTNodeType.METHOD_INVOCATION)
        for node in nodes:
            cur_line = self.get_line_number(node, tree)
            children = tree.children_with_type(node, ASTNodeType.STRING)
            for child in children:
                cur_node = tree.tree.nodes[child]
                if cur_node['type'] == ASTNodeType.STRING and cur_node['string'] == 'isInstance':
                    lines.append(cur_line)
        return lines

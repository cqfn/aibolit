from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType
from networkx import dfs_labeled_edges


class InstanceOf:
    def __init__(self):
        pass

    def __traverse_node(self, node):
        """
        Traverse over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        lines = []
        depth = 0
        cur_line = 0
        bin_depth = -10
        m_depth = -10
        for _, destination, edge_type in dfs_labeled_edges(node.tree, node.root):
            cur_node = node.tree.nodes[destination]
            if edge_type == 'forward':
                cur_node = node.tree.nodes[destination]
                node_type = cur_node['type']
                if 'source_code_line' in cur_node:
                    cur_line = cur_node['source_code_line']
                if node_type == ASTNodeType.BINARY_OPERATION:
                    bin_depth = depth
                if node_type == ASTNodeType.STRING and cur_node['string'] == 'instanceof' and depth - bin_depth == 1:
                    lines.append(cur_line)
                    bin_depth = -10
                if node_type == ASTNodeType.METHOD_INVOCATION:
                    m_depth = depth
                if node_type == ASTNodeType.STRING and cur_node['string'] == 'isInstance' and depth - m_depth == 1:
                    lines.append(cur_line)
                    m_depth = -10
                depth += 1
            elif edge_type == 'reverse':
                depth -= 1
        return lines

    def value(self, filename: str):
        tree = AST(build_ast(filename))
        return self.__traverse_node(tree)

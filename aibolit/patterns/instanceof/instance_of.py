from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType
from networkx import dfs_labeled_edges # type: ignore


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
        lines = []
        depth = 0
        cur_line = 0
        bin_depth = 0
        m_depth = 0
        for _, destination, edge_type in dfs_labeled_edges(tree.tree, tree.root):
            if edge_type == 'forward':
                cur_node = tree.tree.nodes[destination]
                node_type = cur_node['type']
                if 'source_code_line' in cur_node:
                    cur_line = cur_node['source_code_line']
                if node_type == ASTNodeType.BINARY_OPERATION:
                    bin_depth = depth
                if node_type == ASTNodeType.STRING and cur_node['string'] == 'instanceof' and depth - bin_depth == 1:
                    lines.append(cur_line)
                    bin_depth = 0
                if node_type == ASTNodeType.METHOD_INVOCATION:
                    m_depth = depth
                if node_type == ASTNodeType.STRING and cur_node['string'] == 'isInstance' and depth - m_depth == 1:
                    lines.append(cur_line)
                    m_depth = 0
                depth += 1
            elif edge_type == 'reverse':
                depth -= 1
        return lines

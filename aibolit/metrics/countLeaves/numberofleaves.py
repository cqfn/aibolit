import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List


class CountNumberOfLeaves:
    '''
    Returns number of leaves in class (sum by each method).
    input: file_path
    output: sum of leaves in class by each method
    '''
    def __init__(self):
        pass

    def value(self, filename: str):

        tree = JavalangImproved(filename)

        nodes = tree.tree_to_nodes()
        traversed = []
        for each_node in nodes:
            if type(each_node.node) == javalang.tree.MethodDeclaration:
                traversed.append(countLeaves(each_node.node.body))

        return sum(traversed)


def countLeaves(root):
    # forming the same data type for each object
    root_arr = root if isinstance(root, List) else [root]
    leaves = 0
    not_count = [None, '', set()]

    # traverse through all childs of object. If there is no child, hence we faced leaf
    for node in root_arr:

        if not hasattr(node, 'children') and node not in not_count:
            return leaves + 1

        elif node in not_count:
            continue

        for each_child in node.children:
            leaves += countLeaves(each_child)

    return leaves

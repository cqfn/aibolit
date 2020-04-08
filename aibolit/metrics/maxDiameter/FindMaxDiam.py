import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List


class MaxDiamOfTree:
    '''
    Returns max diameter for each method.
    This value is sum of Height of highest two subtree + 1
    '''
    def __init__(self):
        pass

    def value(self, filename: str):

        tree = JavalangImproved(filename)
        nodes = tree.tree_to_nodes()

        traversed = []
        for each_noda in nodes:
            if type(each_noda.node) == javalang.tree.MethodDeclaration:
                traversed.append(diameter(each_noda.node))

        return max(traversed)


def depthOfTree(node):
    '''
    Utility function that will return the depth of the tree
    '''
    maxdepth = 0
    if isinstance(node, List):
        for each_child in node:
            maxdepth = max(maxdepth, depthOfTree(each_child)) - 1
    else:
        try:
            # Check for all children and find the maximum depth
            for each_child in node.children:
                maxdepth = max(maxdepth, depthOfTree(each_child))
        except:
            return 0

    return maxdepth + 1


def diameter(root):
    '''
    Function to calculate the diameter of the tree
    '''
    # Find top two highest children
    max1 = 0
    max2 = 0
    if isinstance(root, List):
        for each_child in root:
            diameter(each_child)
    else:
        try:
            # Iterate over each child for diameter
            for each_child in root.children:
                h = depthOfTree(each_child)
                if h > max1:
                    max2 = max1
                    max1 = h
                elif h > max2:
                    max2 = h
        except:
            return 0

    maxChildDia = 0
    if isinstance(root, List):
        for each_child in root:
            maxChildDia = max(maxChildDia, diameter(each_child))
    else:
        try:
            for each_child in root.children:
                maxChildDia = max(maxChildDia, diameter(each_child))
        except:
            return 0

    return max(maxChildDia, max1 + max2 + 1)

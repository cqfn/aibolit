from aibolit.utils.ast_builder import build_ast

from javalang.tree import MethodDeclaration, ClassDeclaration
from typing import Type


class MaxDiamOfTree:
    '''
    Returns max diameter for each method.
    This value is sum of Height of highest two subtree + 1
    '''
    def __init__(self):
        pass

    def depthOfTree(self, node: Type) -> int:
        '''
        Utility function that will return the depth of the tree
        '''
        maxdepth = 0

        node_arr = node if isinstance(node, list) else [node]
        for child in node_arr:
            if not hasattr(child, 'children'):
                return 0

            # Check for all children and find the maximum depth
            for each_child in child.children:
                maxdepth = max(maxdepth, self.depthOfTree(each_child))

        return maxdepth + 1

    def diameter(self, root: MethodDeclaration) -> int:
        '''
        Function to calculate the diameter of the tree
        '''
        # Find top two highest children
        max1 = 0
        max2 = 0
        root_arr = root if isinstance(root, list) else [root]
        for child in root_arr:
            if not hasattr(child, 'children'):
                return 0

            # Iterate over each child for diameter
            for each_child in child.children:
                h = self.depthOfTree(each_child)
                if h > max1:
                    max2 = max1
                    max1 = h
                elif h > max2:
                    max2 = h

        maxChildDia = 0
        for child in root_arr:
            if not hasattr(child, 'children'):
                return 0

            for each_child in child.children:
                maxChildDia = max(maxChildDia, self.diameter(each_child))

        return max(maxChildDia, max1 + max2 + 1)

    def value(self, filename: str):
        tree = build_ast(filename)

        traversed = []
        for _, class_body in tree.filter(ClassDeclaration):
            for each_object in class_body.body:
                if isinstance(each_object, MethodDeclaration):
                    traversed.append(self.diameter(each_object))

        return max(traversed, default=0)

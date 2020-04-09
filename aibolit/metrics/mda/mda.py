from aibolit.utils.ast import AST


class MaxDepth():


    def __init__(self, filename):
        """Initialize class."""
        if len(filename) == 0:
            raise ValueError('Empty file for analysis')
        self.filename = filename

    def get_depth(self, tree):
        result = 0
        max_val = 0

        if tree is None:
            return 0
        elif type(tree) is list:
            children = tree
        elif type(tree) is set:
            children = tree
        elif type(tree) is tuple:
            children = tree
        elif not hasattr(tree, "children"):
            return 0
        else:
            children = tree.children
            result = 1

        for child in children:
            cur_val = self.get_depth(child)
            if cur_val > max_val:
                max_val = cur_val
        return max_val + result

    def value(self):
        tree = AST(self.filename).value()
        return self.get_depth(tree)
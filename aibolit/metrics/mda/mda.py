from aibolit.utils.ast import AST


class MDAMetric:
    @staticmethod
    def get_depth(tree) -> int:
        result = 0
        max_val = 0

        if tree is None:
            return 0
        elif isinstance(tree, (list, set, tuple)):
            children = tree
        elif not hasattr(tree, "children"):
            return 0
        else:
            children = tree.children
            result = 1

        for child in children:
            cur_val = MDAMetric.get_depth(child)
            if cur_val > max_val:
                max_val = cur_val
        return max_val + result

    @staticmethod
    def value(filename: str) -> int:
        tree = AST(filename).value()
        metric = MDAMetric.get_depth(tree)

        return metric

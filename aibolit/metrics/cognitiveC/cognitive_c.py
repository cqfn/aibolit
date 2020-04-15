import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List

increment_for = [
    javalang.tree.IfStatement,
    javalang.tree.SwitchStatement,
    javalang.tree.ForStatement,
    javalang.tree.WhileStatement,
    javalang.tree.DoStatement,
    javalang.tree.CatchClause,
    javalang.tree.BreakStatement,
    javalang.tree.ContinueStatement,
    javalang.tree.TernaryExpression,
    # javalang.tree.BinaryOperation,
]

nested_for = [
    javalang.tree.IfStatement,
    javalang.tree.SwitchStatement,
    javalang.tree.ForStatement,
    javalang.tree.WhileStatement,
    javalang.tree.DoStatement,
    javalang.tree.CatchClause,
]


class CognitiveComplexity:
    '''
    beta version of Cognitive Complexity
    '''
    def __init__(self):
        self.complexity = 0

    def test(self, childs, nested_level=0):
        child_arr = childs if isinstance(childs, List) else [childs]

        for c in child_arr:

            if hasattr(c, 'children'):
                if type(c) in increment_for and type(c) in nested_for:
                    self.complexity += (1 + nested_level)
                    for each_child in c.children:
                        self.test(each_child, nested_level + 1)

                elif type(c) in increment_for and type(c) not in nested_for:
                    self.complexity += 1
                    for each_child in c.children:
                        self.test(each_child, nested_level)
                else:
                    for each_child in c.children:
                        self.test(each_child, nested_level)

            continue

    def value(self, filename: str):

        nodes = JavalangImproved(filename).tree_to_nodes()

        for i in nodes:
            if type(i.node) in [javalang.tree.MethodDeclaration]:
                self.test(i.node)

        final_value = self.complexity
        self.complexity = 0
        return final_value

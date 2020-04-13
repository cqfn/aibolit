import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved
from typing import List


class CognitiveComplexity:
    '''
    beta version of Cognitive Complexity
    '''
    def __init__(self):
        pass

    def if_statements(self, nodes: List) -> int:
        count = 0
        for i in nodes:
            if type(i.node) in [javalang.tree.IfStatement]:
                count += 1
        return count

    def for_statements(self, nodes: List) -> int:
        count = 0
        for i in nodes:
            if type(i.node) in [javalang.tree.ForStatement]:
                count += 1
        return count

    def value(self, filename: str):

        nodes = JavalangImproved(filename).tree_to_nodes()

        rules = [self.if_statements, self.for_statements]
        complexity = 0

        for rule in rules:
            complexity += rule(nodes)

        return complexity

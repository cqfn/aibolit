import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved


class CognitiveComplexity:
    '''
    beta version of Cognitive Complexity
    '''
    def __init__(self):
        pass

    def If_statements(self, nodes):
        count = 0
        for i in nodes:
            if type(i.node) in [javalang.tree.IfStatement]:
                count += 1
        return count

    def For_statements(self, nodes):
        count = 0
        for i in nodes:
            if type(i.node) in [javalang.tree.ForStatement]:
                count += 1
        return count

    def value(self, filename: str):

        nodes = JavalangImproved(filename).tree_to_nodes()

        rules = [self.If_statements, self.For_statements]
        complexity = 0

        for rule in rules:
            complexity += rule(nodes)

        return complexity

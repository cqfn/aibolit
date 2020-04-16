import javalang
from aibolit.utils.ast import AST
from typing import List, Any, Type

increment_for: List[Type] = [
    javalang.tree.IfStatement,
    javalang.tree.SwitchStatement,
    javalang.tree.ForStatement,
    javalang.tree.WhileStatement,
    javalang.tree.DoStatement,
    javalang.tree.CatchClause,
    javalang.tree.BreakStatement,
    javalang.tree.ContinueStatement,
    javalang.tree.TernaryExpression,
    javalang.tree.BinaryOperation,
]

nested_for: List[Type] = [
    javalang.tree.IfStatement,
    javalang.tree.SwitchStatement,
    javalang.tree.ForStatement,
    javalang.tree.WhileStatement,
    javalang.tree.DoStatement,
    javalang.tree.CatchClause,
]

logical_operators = ['&', '&&', '^', '|', '||']


class CognitiveComplexity:
    '''
    beta version of Cognitive Complexity
    '''
    def __init__(self):
        self.complexity = 0

    def traverse_childs(self, block: Any, nested_level: int):

        for each_child in block.children:
            self.get_complexity(each_child, nested_level)

    def increment_logical_operators(self, block: Type, prev_operator: str):
        for each_block in [block.operandr, block.operandl]:

            if isinstance(each_block, javalang.tree.BinaryOperation) and prev_operator in logical_operators:
                if prev_operator != each_block.operator:
                    self.complexity += 1

                elif isinstance(each_block.operandr, javalang.tree.BinaryOperation):
                    self.complexity += 1

                self.increment_logical_operators(each_block, each_block.operator)

    def get_complexity(self, block: Any, nested_level: int):
        block_arr = block if isinstance(block, List) else [block]

        for each_block in block_arr:
            if hasattr(each_block, 'children'):
                if type(each_block) in increment_for and type(each_block) in nested_for:
                    self.complexity += 1 + nested_level
                    self.traverse_childs(each_block, nested_level + 1)

                elif type(each_block) in increment_for and type(each_block) not in nested_for:
                    if isinstance(each_block, javalang.tree.BinaryOperation):
                        if each_block.operator in logical_operators:
                            self.complexity += 1
                            self.increment_logical_operators(each_block, each_block.operator)

                        continue

                    self.complexity += 1
                    self.traverse_childs(each_block, nested_level)
                else:
                    self.traverse_childs(each_block, nested_level)

            continue

    def value(self, filename: str) -> int:

        tree = AST(filename).value()
        for _, method in tree.filter(javalang.tree.MethodDeclaration):
            self.get_complexity(method, 0)

        final_value, self.complexity = self.complexity, 0
        return final_value

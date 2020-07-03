from itertools import groupby

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_package import JavaPackage
from typing import List, Any

increment_for: List[ASTNodeType] = [
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT,
    ASTNodeType.FOR_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
    ASTNodeType.BREAK_STATEMENT,
    ASTNodeType.CONTINUE_STATEMENT,
    ASTNodeType.TERNARY_EXPRESSION,
    ASTNodeType.BINARY_OPERATION,
    ASTNodeType.METHOD_INVOCATION,
]

nested_for: List[ASTNodeType] = [
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT,
    ASTNodeType.FOR_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
]

logical_operators = ['&&', '||']


class CognitiveComplexity:

    def __init__(self):
        self.complexity = 0
        self.method_name = None

    def _traverse_childs(self, ast, node: Any, nested_level: int) -> None:
        for each_child in ast.tree.succ[node]:
            #print(ast.get_type(node), ast.get_type(each_child))
            self._get_complexity(ast, each_child, nested_level)

    def _check_if_statement(self, ast, expr, nested_level: int) -> None:
        '''function to work with IfStatement block'''
        bin_statement = list(ast.children_with_type(expr, ASTNodeType.BINARY_OPERATION))
        if len(bin_statement) != 0:
            self._get_complexity(ast, bin_statement[0], 0)

        nested_statements = list(ast.children_with_type(expr, ASTNodeType.BLOCK_STATEMENT))
        elif_statements = list(ast.children_with_type(expr, ASTNodeType.IF_STATEMENT))

        for i in elif_statements:
            self.complexity += 1
            self._check_if_statement(ast, i, nested_level)

        for j in nested_statements:
            self.complexity += nested_level + 1
            self._get_complexity(ast, j, nested_level + 1)

    def _increment_logical_operators(self, ast: AST, binary_operation_node: int) -> None:
        logical_operators_sequence = self._create_logical_operators_sequence(ast, binary_operation_node)
        self.complexity += len(list(groupby(logical_operators_sequence)))

    def _create_logical_operators_sequence(self, ast: AST, binary_operation_node: int) -> List[str]:
        if ast.get_type(binary_operation_node) != ASTNodeType.BINARY_OPERATION:
            return []

        operator, left_side_node, right_side_node = ast.get_binary_operation_params(binary_operation_node)
        if operator not in logical_operators:
            return []

        left_sequence = self._create_logical_operators_sequence(ast, left_side_node)
        right_sequence = self._create_logical_operators_sequence(ast, right_side_node)
        return left_sequence + [operator] + right_sequence

    def _is_recursion_call(self, ast, node) -> bool:
        if ast.get_type(node) == ASTNodeType.METHOD_INVOCATION:
            if self.method_name == self._get_node_name(ast, node):
                return True
            return False

    def _nested_methods(self, ast, node, nested_level: int) -> None:
        original_name = self.method_name
        self.method_name = self._get_node_name(ast, node)
        self._get_complexity(ast, node, nested_level + 1)
        self.method_name = original_name

    def _get_complexity(self, ast: Any, node: int, nested_level: int) -> None:

        for each_block in ast.tree.succ[node]:
            each_block_name = self._get_node_name(ast, each_block)
            each_block_type = ast.get_type(each_block)

            if each_block_type == ASTNodeType.METHOD_DECLARATION and each_block_name != self.method_name:
                self._nested_methods(ast, each_block, nested_level)

            elif each_block_type == ASTNodeType.IF_STATEMENT:
                self.complexity += 1
                self._get_complexity(ast, each_block, nested_level + 1)

            elif each_block_type in increment_for and each_block_type in nested_for:
                self.complexity += 1 + nested_level
                self._get_complexity(ast, each_block, nested_level + 1)

            elif each_block_type in increment_for and each_block_type not in nested_for:
                if ast.get_type(each_block) == ASTNodeType.BINARY_OPERATION:
                    bin_operator = ast.get_binary_operation_name(each_block)
                    if bin_operator in logical_operators:
                        self.complexity += 1
                        self._increment_logical_operators(ast, each_block)
                elif each_block_type == ASTNodeType.METHOD_INVOCATION:
                    is_recursion = self._is_recursion_call(ast, each_block)
                    self.complexity += is_recursion

                else:
                    self.complexity += 1
                    self._get_complexity(ast, each_block, nested_level)

            else:
                self._get_complexity(ast, each_block, nested_level)

    def _get_node_name(self, ast, node) -> str:
        extracted_name = None
        names = list(ast.children_with_type(node, ASTNodeType.STRING))
        for each_string in names:
            method_name = ast.get_attr(each_string, 'string')
            if not method_name.startswith('/') and method_name not in ['', None, []]:
                extracted_name = method_name
                return extracted_name

    def value(self, filename: str) -> int:
        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            declareted_methods = tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION)
            for class_method in declareted_methods:
                ast_each_method = AST(tree.tree.subgraph(class_method), class_method[0])
                self.method_name = self._get_node_name(ast_each_method, ast_each_method.root)
                self._get_complexity(ast_each_method, class_method[0], 0)
                print(self.method_name)

        return self.complexity


filename = '../test.java'
CognitiveComplexity().value(filename)

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_package import JavaPackage
from typing import List, Any, Type

increment_for: List[Type] = [
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

nested_for: List[Type] = [
    ASTNodeType.IF_STATEMENT,
    ASTNodeType.SWITCH_STATEMENT,
    ASTNodeType.FOR_STATEMENT,
    ASTNodeType.WHILE_STATEMENT,
    ASTNodeType.DO_STATEMENT,
    ASTNodeType.CATCH_CLAUSE,
]

logical_operators: List[str] = ['&', '&&', '^', '|', '||']


class CognitiveComplexity:

    def __init__(self):
        self.complexity = 0
        self.method_name = None

    def _traverse_childs(self, ast, node: Any, nested_level: int) -> None:

        for each_child in ast.tree.succ[node]:
            self._get_complexity(ast, each_child, nested_level)
    '''
    def _check_if_statement(self, ast, expr, nested_level: int) -> None:
        '''function to work with IfStatement block'''
        bin_operation_ = list(ast.children_with_type(expr, ASTNodeType.BINARY_OPERATION))
        self._get_complexity(ast, bin_operation_[0], 0)
        if expr.then_statement is not None:
            self.complexity += nested_level + 1
            self._get_complexity(expr.then_statement, nested_level + 1)

        if expr.else_statement is not None:
            if isinstance(expr.else_statement, IfStatement):
                self.complexity -= nested_level
                self._check_if_statement(expr.else_statement, nested_level)
            else:
                self.complexity += 1
                self._get_complexity(expr.else_statement, nested_level + 1)
    '''
    def _increment_logical_operators(self, block: BinaryOperation, prev_operator: str) -> None:
        print('_increment_logical_operators')
        return
    
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
            
            elif each_block_type ==  ASTNodeType.IF_STATEMENT:
                self._check_if_statement(ast, each_block, nested_level)

            elif each_block_type in increment_for and each_block_type in nested_for:
                self.complexity += 1 + nested_level
                self._traverse_childs(ast, each_block, nested_level + 1)
            
            elif each_block_type in increment_for and each_block_type not in nested_for:
                if ast.get_type(each_block) == ASTNodeType.BINARY_OPERATION:
                    bin_operator = ast.get_binary_operation_name(each_block)
                    if bin_operator in logical_operators:
                        self.complexity += 1
                        self._increment_logical_operators(ast, each_block, bin_operator)
                elif each_block_type == ASTNodeType.METHOD_INVOCATION:
                    is_recursion = self._is_recursion_call(ast, each_block)
                    self.complexity += is_recursion

                else:
                    self.complexity += 1
                    self._traverse_childs(ast, each_block, nested_level)

            else:
                self._traverse_childs(ast, each_block, nested_level)
            
    
    def _get_node_name(self, ast, node) -> str:
        extracted_name = None
        names = list(ast.children_with_type(node, ASTNodeType.STRING))
        for each_string in names:
            method_name = ast.get_attr(each_string, 'string')
            if not method_name.startswith('/'):
                extracted_name = method_name
                return extracted_name
        
    def value(self, filename: str) -> int:
        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            print(tree)
            declareted_methods = tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION)
            for class_method in declareted_methods:
                ast_each_method = AST(tree.tree.subgraph(class_method), class_method[0])
                self.method_name = self._get_node_name(ast_each_method, ast_each_method.root)
                self._get_complexity(ast_each_method, class_method[0], 0)
                print(self.method_name)
        
        return self.complexity

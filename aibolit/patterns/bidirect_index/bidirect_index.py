# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import ast
from typing import List, Dict, Set, Optional


class BidirectIndex:

    def __init__(self):
        pass

    def value(self, filename: str | os.PathLike) -> List['LineNumber']:
        """
        Finds if a variable is being incremented and decremented within the same method

        :param filename: filename to be analyzed
        :return: list of LineNumber with the variable declaration lines
        """
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            source_code = file.read()
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []
        detector = BidirectIndexDetector()
        detector.visit(tree)
        return detector.bidirect_vars()


class LineNumber:
    def __init__(self, line: int, variable: str):
        self.line = line
        self.variable = variable

    def __repr__(self):
        return f"LineNumber(line={self.line}, variable='{self.variable}')"

    def __eq__(self, other):
        if not isinstance(other, LineNumber):
            return False
        return self.line == other.line and self.variable == other.variable


class BidirectIndexDetector(ast.NodeVisitor):
    def __init__(self, bvars: List, method:  Optional[str], ops, mvars: Dict):
        self.bidirect_variables = bvars
        self.current_method = method
        self.method_operations = ops
        self.method_variables = mvars

    def visit_FunctionDef(self, node):
        prev = self.current_method
        self.current_method = node.name
        self.method_operations[self.current_method] = {}
        self.method_variables[self.current_method] = {}
        self._find_variable_declarations(node)        
        self.generic_visit(node)
        self._check_bidirectional_variables()
        self.current_method = prev

    def _find_variable_declarations(self, node):
        """Find all variable declarations in the function"""
        for child in ast.walk(node):
            if isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        if var_name not in self.method_variables[self.current_method]:
                            self.method_variables[self.current_method][var_name] = child.lineno
            elif isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                var_name = child.target.id
                if var_name not in self.method_variables[self.current_method]:
                    self.method_variables[self.current_method][var_name] = child.lineno
            elif isinstance(child, ast.AugAssign) and isinstance(child.target, ast.Name):
                var_name = child.target.id
                if var_name not in self.method_variables[self.current_method]:
                    self.method_variables[self.current_method][var_name] = child.lineno

    def visit_AugAssign(self, node):
        if self.current_method is None or not isinstance(node.target, ast.Name):
            return            
        var_name = node.target.id
        operation = self._get_aug_operation_type(node.op)
        if operation:
            if var_name not in self.method_operations[self.current_method]:
                self.method_operations[self.current_method][var_name] = set()
            self.method_operations[self.current_method][var_name].add(operation)

    def visit_Assign(self, node):
        if self.current_method is None:
            return            
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                operation = self._get_assign_operation_type(node.value, var_name)
                if operation:
                    if var_name not in self.method_operations[self.current_method]:
                        self.method_operations[self.current_method][var_name] = set()
                    self.method_operations[self.current_method][var_name].add(operation)

    def visit_UnaryOp(self, node):
        if self.current_method is None or not isinstance(node.operand, ast.Name):
            return            
        var_name = node.operand.id
        operation = self._get_unary_operation_type(node.op)
        if operation:
            if var_name not in self.method_operations[self.current_method]:
                self.method_operations[self.current_method][var_name] = set()
            self.method_operations[self.current_method][var_name].add(operation)

    def _get_aug_operation_type(self, op) -> Optional[str]:
        """Get operation type for augmented assignment"""
        if isinstance(op, ast.Add):
            return 'increment'
        elif isinstance(op, ast.Sub):
            return 'decrement'
        return None

    def _get_assign_operation_type(self, value, var_name: str) -> Optional[str]:
        """Get operation type for regular assignment"""
        if isinstance(value, ast.BinOp):
            if (isinstance(value.left, ast.Name) and value.left.id == var_name):
                if isinstance(value.op, ast.Add):
                    return 'increment'
                elif isinstance(value.op, ast.Sub):
                    return 'decrement'
            elif (isinstance(value.right, ast.Name) and value.right.id == var_name and 
                  isinstance(value.op, ast.Add)):
                return 'increment'
        return None

    def _get_unary_operation_type(self, op) -> Optional[str]:
        """Get operation type for unary operations"""
        if isinstance(op, ast.UAdd):
            return 'increment'
        elif isinstance(op, ast.USub):
            return 'decrement'
        return None

    def _check_bidirectional_variables(self):
        """Check for bidirectional variables in the current method"""
        if self.current_method not in self.method_operations:
            return
            
        method_ops = self.method_operations[self.current_method]
        method_vars = self.method_variables[self.current_method]
        
        for var_name, operations in method_ops.items():
            if 'increment' in operations and 'decrement' in operations:
                if var_name in method_vars:
                    decl_line = method_vars[var_name]
                    self.bidirect_variables.append(LineNumber(decl_line, var_name))

    def bidirect_vars(self) -> List[LineNumber]:
        return self.bidirect_variables

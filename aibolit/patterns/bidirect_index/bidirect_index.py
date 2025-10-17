# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import ast
from typing import List, Dict


class BidirectIndex:

    def __init__(self):
        pass

    def value(self, filename: str | os.PathLike):
        """
        Finds if a variable is being incremented and decremented within the same method

        :param filename: filename to be analyzed
        :return: list of LineNumber with the variable declaration lines

        @todo #139:30min Implement bidirect index pattern
        If the same numeric variable is incremented and decremented within the same method,
        it's a pattern. A numeric variable should either be always growing or decreasing.
        Bi-directional index is confusing. The method must return a list with the line numbers
        of the variables that match this pattern. After implementation, activate tests in
        test_bidirect_index.py
        """
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            source_code = file.read()
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []
        detector = BidirectIndexDetector([], '', {})
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
    def __init__(self, vars: List, method: str = '', ops: Dict):
        self.bidirect_variables = vars
        self.current_method = method
        self.method_operations = ops

    def visit_FunctionDef(self, node):
        self.current_method = node.name
        self.method_operations[self.current_method] = {}
        self.generic_visit(node)
        self._check_bidirectional_variables(node)
        self.current_method = None

    def visit_ClassDef(self, node):
        pass

    def visit_AugAssign(self, node):
        if self.current_method is None:
            return
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            operation = self._operation_type(node.op)
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
                if (isinstance(node.value, ast.BinOp) and
                        isinstance(node.value.left, ast.Name) and
                        node.value.left.id == var_name):
                    operation = self._binop_operation_type(node.value.op)
                    if operation:
                        if var_name not in self.method_operations[self.current_method]:
                            self.method_operations[self.current_method][var_name] = set()
                        self.method_operations[self.current_method][var_name].add(operation)

    def _operation_type(self, op) -> str | None:
        if isinstance(op, ast.Add):
            return 'increment'
        elif isinstance(op, ast.Sub):
            return 'decrement'
        return None

    def _binop_operation_type(self, op) -> str | None:
        return self._operation_type(op)

    def _check_bidirectional_variables(self, node):
        method_ops = self.method_operations.get(self.current_method, {})
        for var_name, operations in method_ops.items():
            if 'increment' in operations and 'decrement' in operations:
                decl_line = self._find_variable_declaration(node, var_name)
                if decl_line:
                    self.bidirect_variables.append(LineNumber(decl_line, var_name))

    def _find_variable_declaration(self, node, var_name: str) -> int | None:
        for stmt in ast.walk(node):
            if isinstance(stmt, (ast.AnnAssign, ast.Assign, ast.AugAssign)):
                targets = []
                if isinstance(stmt, ast.Assign):
                    targets = stmt.targets
                elif isinstance(stmt, (ast.AnnAssign, ast.AugAssign)):
                    targets = [stmt.target]
                for target in targets:
                    if isinstance(target, ast.Name) and target.id == var_name:
                        return stmt.lineno
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Name) and stmt.id == var_name:
                return stmt.lineno
        return None

    def bidirect_vars(self) -> List[LineNumber]:
        return self.bidirect_variables

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import ast
from typing import List, Union, Set, Dict

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
        detector = BidirectIndexDetector()
        detector.visit(tree)        
        return detector.get_bidirect_variables()


class BidirectIndexDetector(ast.NodeVisitor):
    def __init__(self):
        self.bidirect_variables: List[LineNumber] = []
        self.current_method: str = None
        self.method_operations: Dict[str, Dict[str, Set[str]]] = {}
    
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
            operation = self._get_operation_type(node.op)            
            if operation:
                if var_name not in self.method_operations[self.current_method]:
                    self.method_operations[self.current_method][var_name] = set()                
                self.method_operations[self.current_method][var_name].add(operation)


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

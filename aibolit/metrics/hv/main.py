# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import ast
import math
from typing import Dict, List, Set, Tuple


class HVMetric:
     """Main Halstead Volume class."""

    def __init__(self, filename: str):
        self.filename = filename
    
    def value(self) -> Dict:
        """Calculate Halstead Volume metric."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                source_code = file.read()            
            if not source_code.strip():
                return {'error': 'Empty file for analysis'}            
            operators, operands = self._parse_code(source_code)
            n1 = len(operators)
            n2 = len(operands)
            N1 = sum(operators.values())
            N2 = sum(operands.values())            
            if n1 + n2 == 0:
                halstead_volume = 0.0
            else:
                halstead_volume = (N1 + N2) * math.log2(n1 + n2)            
            return {
                'data': [{
                    'file': self.filename,
                    'halstead_volume': halstead_volume,
                    'distinct_operators': n1,
                    'distinct_operands': n2,
                    'total_operators': N1,
                    'total_operands': N2
                }]
            }            
        except FileNotFoundError:
            return {'error': f'File not found: {self.filename}'}
        except Exception as e:
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _parse_code(self, source_code: str) -> Tuple[Dict[str, int], Dict[str, int]]:
        """Parse source code and extract operators and operands."""

        operators = {}
        operands = {}
        common_operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', 
                           'and', 'or', 'not', 'in', 'is'}
        tokens = source_code.split()
        for token in tokens:
            clean_token = token.strip('.,;(){}[]')            
            if clean_token in common_operators:
                operators[clean_token] = operators.get(clean_token, 0) + 1
            elif clean_token and clean_token[0].isalnum():
                operands[clean_token] = operands.get(clean_token, 0) + 1        
        return operators, operands

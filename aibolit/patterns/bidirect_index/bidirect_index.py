# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import ast

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
        return []


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

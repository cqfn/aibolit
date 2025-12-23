# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
import re

from aibolit.types_decl import LineNumber


class BidirectIndex:
    """
    Analyze Java source code to find line numbers where a variable is used as a bidirectional index.

    A bidirectional index is a variable that:
      - is assigned a value (with or without type declaration) within a method or block,
      - is incremented and decremented somewhere in its scope,
      - increments/decrements inside a for-loop with a local variable of the same name are ignored.

    Usage:
        idx = BidirectIndex()
        result = idx.value("MyClass.java")
    """

    def value(self, filename: str | os.PathLike) -> list[LineNumber]:
        """
        Analyze the given Java file and return a sorted list of line numbers where a variable
        is used as a bidirectional index.

        Args:
            filename (str | os.PathLike): Path to the Java source file.

        Returns:
            list[LineNumber]: Sorted list of line numbers where bidirectional indices are found.
        """
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
        result: list[int] = []
        for m_start, m_end in self._find_methods(lines):
            self._analyze_block(lines, m_start + 1, m_end, result)
        return [LineNumber(n) for n in sorted(result)]

    def _find_methods(self, lines):
        """
        Find the start and end line indices (0-based) for each Java method in the file.

        Args:
            lines (list[str]): The lines of the Java source file to analyze.

        Returns:
            list[tuple[int, int]]: Each tuple is (start_line_idx, end_line_idx) for a method.
        """
        res = []
        brace = 0
        mstart = None
        # Regular expression to find method declaration in Java
        method_pattern = re.compile(r'''
            (public|private|protected|static|\s)*  # access modifiers and static
            ([\w<>\[\]]+)                          # return type
            \s+                                    # space
            \w+                                    # method name
            \s*                                    # possible spaces
            \( [^)]* \)                            # parameters in brackets
            \s* \{                                 # opening curly brace
            ''', re.VERBOSE)
        for idx, line in enumerate(lines):
            if method_pattern.search(line):
                if mstart is None:
                    mstart = idx
                    brace = 0
            brace += line.count('{')
            brace -= line.count('}')
            if mstart is not None and brace == 0:
                res.append((mstart, idx))
                mstart = None
        return res

    def _analyze_block(self, lines, start, end, result):
        """
        Recursively analyze a block of code between 'start' and 'end' (inclusive).
        """
        i = start
        while i <= end:
            line = lines[i]
            # Finding a variable declaration with type
            typed_decl = re.match(
                r'\s*(int|long|byte|short)\s+(\w+)\s*=', line)
            # Finding a simple assignment without a type
            untyped_decl = re.match(
                r'^\s*(\w+)\s*=\s*[^=;]+;', line) if not typed_decl else None
            var = typed_decl.group(2) if typed_decl else (untyped_decl.group(1)
                                                          if untyped_decl else None)
            if var:
                j = i + 1
                while j <= end:
                    line_ = lines[j]
                    # Check for both typed declarations and simple reassignments
                    if re.match(
                            r'\s*(int|long|byte|short)\s+' + re.escape(var) + r'\s*=', line_):
                        break
                    j += 1
                inc_outside, dec_outside = (
                    self._count_inc_dec(lines, var, i + 1, j - 1))
                if inc_outside and dec_outside:
                    result.append(i + 1)
            if '{' in line:
                brace, block_start = 1, i
                i += 1
                while i <= end:
                    brace += lines[i].count('{')
                    brace -= lines[i].count('}')
                    if brace == 0:
                        self._analyze_block(lines, block_start + 1, i - 1, result)
                        break
                    i += 1
            else:
                i += 1

    def _find_for_blocks(self, lines, var, start, end):
        """
        Find all ranges of for-loops that declare a local variable with the given name.
        """
        for_blocks = []
        k = start
        # Regular expression to find variable declaration in for
        for_pattern = re.compile(r'''
            \s*for\s*                # keyword for
            \(                       # opening parenthesis
            \s*(int|long|byte|short) # variable type
            \s+''' + re.escape(var) + r'''\s*= # variable name and =
            ''', re.VERBOSE)
        while k < end:
            line_ = lines[k]
            if for_pattern.match(line_):
                brace = line_.count('{') - line_.count('}')
                bstart = k
                k += 1
                while k < end and brace > 0:
                    brace += lines[k].count('{') - lines[k].count('}')
                    k += 1
                for_blocks.append((bstart, k - 1))
                continue
            k += 1
        return for_blocks

    def _count_inc_dec(self, lines, var, start, end):
        """
        Count increments and decrements of variable `var` outside any for-blocks.
        """
        for_blocks = self._find_for_blocks(lines, var, start, end)
        inc_outside = 0
        dec_outside = 0
        k = start
        # Regular expressions for increment and decrement
        inc_pattern = re.compile(r'''
            (\+\+''' + re.escape(var) + r'''|   # ++var
            ''' + re.escape(var) + r'''\+\+|    # var++
            ''' + re.escape(var) + r'''\s*\+=\s*1\b| # var += 1
            ''' + re.escape(var) + r'''\s*=\s*''' + re.escape(var) + r'''\s*\+\s*1\b)# var = var + 1
            ''', re.VERBOSE)
        dec_pattern = re.compile(r'''
            (--''' + re.escape(var) + r'''|     # --var
            ''' + re.escape(var) + r'''--|      # var--
            ''' + re.escape(var) + r'''\s*-=\s*1\b| # var -= 1
            ''' + re.escape(var) + r'''\s*=\s*''' + re.escape(var) + r'''\s*-\s*1\b)# var = var - 1
            ''', re.VERBOSE)
        while k < end:
            in_for = any(bstart <= k <= bend for (bstart, bend) in for_blocks)
            if not in_for:
                line_ = lines[k]
                if inc_pattern.search(line_):
                    inc_outside += 1
                if dec_pattern.search(line_):
                    dec_outside += 1
            k += 1
        return inc_outside, dec_outside

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re


class BidirectIndex:
    """
    This class analyzes Java source code to find line numbers where a variable
    is used as a bidirectional index.
    A bidirectional index is defined as a variable that:
        - is assigned a value (with or without type declaration) within a method or block,
        - is incremented and decremented somewhere in its scope,
        - increments/decrements inside a for-loop with a local variable of the same name
    are ignored (to avoid "fake" cases).

    The typical use-case: detect patterns like `i = 0; ... ++i; ... --i;`
    in Java code, while ignoring manipulations of `i` inside
    loops where `i` is a local loop variable (e.g., `for (int i = 0; ...) { ... }`).

    Usage:
        idx = BidirectIndex()
        lines = open("MyClass.java", encoding="utf-8").readlines()
        result = idx.value(lines)
        # result is a list of line numbers matching the described pattern
    """

    def __init__(self):
        pass

    def value(self, lines):
        """
        Analyze the given Java file lines and return a sorted list of line numbers where a variable
        is used as a bidirectional index as per the definition above.

        Args:
            lines (list[str]): Lines of the Java source file.

        Returns:
            List[int]: Sorted list of line numbers where bidirectional indices are found.
        """
        result: list[int] = []
        for m_start, m_end in BidirectIndex.find_methods(lines):
            BidirectIndex.analyze_block(lines, m_start + 1, m_end, result)
        return sorted(result)

    @staticmethod
    def find_methods(lines):
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
        for idx, line in enumerate(lines):
            if (re.search(
                    r'(public|private|protected|static|\s)*([\w<>\[\]]+)\s+\w+\s*\([^)]*\)\s*{',
                    line)):
                if mstart is None:
                    mstart = idx
                    brace = 0
            brace += line.count('{')
            brace -= line.count('}')
            if mstart is not None and brace == 0:
                res.append((mstart, idx))
                mstart = None
        return res

    @staticmethod
    def analyze_block(lines, start, end, result):
        """
        Recursively analyze a block of code between 'start' and 'end' (inclusive).
        """
        i = start
        while i <= end:
            line = lines[i]
            typed_decl = re.match(r'\s*(int|long|byte|short)\s+(\w+)\s*=', line)
            untyped_decl = re.match(r'^\s*(\w+)\s*=\s*[^;]+;', line) \
                if not typed_decl else None
            var = typed_decl.group(2) if typed_decl else (untyped_decl.group(1)
                                                          if untyped_decl else None)
            if var:
                j = i + 1
                while j <= end:
                    line_ = lines[j]
                    if re.match(r'\s*(int|long|byte|short)\s+' + re.escape(var) + r'\s*=', line_):
                        break
                    j += 1
                for_blocks = BidirectIndex.find_for_blocks(lines, var, i + 1, j)
                inc_outside, dec_outside = (
                    BidirectIndex.count_inc_dec(lines, var, for_blocks, i + 1, j))
                if inc_outside and dec_outside:
                    result.append(i + 1)
            if '{' in line:
                brace, block_start = 1, i
                i += 1
                while i <= end:
                    brace += lines[i].count('{')
                    brace -= lines[i].count('}')
                    if brace == 0:
                        BidirectIndex.analyze_block(lines, block_start + 1, i - 1, result)
                        break
                    i += 1
            else:
                i += 1

    @staticmethod
    def find_for_blocks(lines, var, start, end):
        """
        Find all ranges of for-loops that declare a local variable with the given name.
        """
        for_blocks = []
        k = start
        while k < end:
            line_ = lines[k]
            for_decl = re.match(r'\s*for\s*\(\s*int\s+' + re.escape(var) + r'\s*=', line_)
            if for_decl:
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

    @staticmethod
    def count_inc_dec(lines, var, for_blocks, start, end):
        """
        Count increments and decrements of variable `var` outside any for-blocks.
        """
        inc_outside = 0
        dec_outside = 0
        k = start
        while k < end:
            in_for = any(bstart <= k <= bend for (bstart, bend) in for_blocks)
            if not in_for:
                line_ = lines[k]
                if re.search(
                        r'(\+\+' + re.escape(var) + r'|' + re.escape(var) + r'\+\+|' +
                        re.escape(var) + r'\s*\+=\s*1\b|' +
                        re.escape(var) + r'\s*=\s*' + re.escape(var) + r'\s*\+\s*1\b)', line_):
                    inc_outside += 1
                if re.search(
                        r'(--' + re.escape(var) + r'|' + re.escape(var) + r'--|' +
                        re.escape(var) + r'\s*-=\s*1\b|' +
                        re.escape(var) + r'\s*=\s*' + re.escape(var) + r'\s*-\s*1\b)', line_):
                    dec_outside += 1
            k += 1
        return inc_outside, dec_outside

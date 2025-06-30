# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
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
        result = idx.value("MyClass.java")
        # result is a list of line numbers matching the described pattern
    """

    def __init__(self):
        pass

    @staticmethod
    def value(filename: str | os.PathLike):
        """
        Analyze the given Java file and return a sorted list of line numbers where a variable
        is used as a bidirectional index as per the definition above.

        Args:
            filename: Path to the Java source file.

        Returns:
            List[int]: Sorted list of line numbers where bidirectional indices are found.
        """
        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()

        result = []

        def methods():
            """
            Find the start and end line indices (0-based) for each method in the file.

            Returns:
                List[Tuple[int, int]]: Each tuple is (start_line_idx, end_line_idx) for a method.
            """
            res = []
            brace = 0
            mstart = None
            for idx, line in enumerate(lines):
                # Detect method start by pattern: 'void methodName(...) {'
                if re.search(r"\bvoid\b\s+\w+\s*\(.*\)\s*{", line):
                    if mstart is None:
                        mstart = idx
                        brace = 0
                brace += line.count("{")
                brace -= line.count("}")
                if mstart is not None and brace == 0:
                    res.append((mstart, idx))
                    mstart = None
            return res

        def analyze_block(start, end):
            """
            Recursively analyze a block of code between line indices `start` and `end` (inclusive)
            for bidirectional index variables.

            Args:
                start (int): Index of the first line of the block.
                end (int): Index of the last line of the block.
            """
            i = start
            while i <= end:
                line = lines[i]
                # 1. Variable declaration with type (e.g., 'int i = 0;')
                typed_decl = re.match(r'\s*(int|long|byte|short)\s+(\w+)\s*=', line)
                # 2. Variable assignment without type (e.g., 'i = 0;')
                # if not already matched as typed
                untyped_decl = re.match(r'^\s*(\w+)\s*=\s*[^;]+;', line) \
                    if not typed_decl else None
                var = None
                if typed_decl:
                    var = typed_decl.group(2)
                elif untyped_decl:
                    var = untyped_decl.group(1)
                if var:
                    # Determine the lifetime of the variable (until next redeclaration or block end)
                    j = i + 1
                    while j <= end:
                        l = lines[j]
                        # Variable shadowing: stop at a new declaration with the same name
                        if re.match(r'\s*(int|long|byte|short)\s+' + re.escape(var) + r'\s*=', l):
                            break
                        j += 1

                    # Identify ranges of for-loops that have a local variable with the same name
                    for_blocks = []
                    k = i + 1
                    while k < j:
                        l = lines[k]
                        for_decl = re.match(r'\s*for\s*\(\s*int\s+' + re.escape(var) + r'\s*=', l)
                        if for_decl:
                            # Find the boundaries of the for-loop block
                            brace = l.count('{') - l.count('}')
                            bstart = k
                            k += 1
                            while k < j and brace > 0:
                                brace += lines[k].count('{') - lines[k].count('}')
                                k += 1
                            for_blocks.append((bstart, k - 1))
                            continue
                        k += 1

                    # Count increments/decrements outside any for-block with local var
                    inc_outside = 0
                    dec_outside = 0
                    k = i + 1
                    while k < j:
                        # Skip lines inside for-blocks with local var
                        in_for = any(bstart <= k <= bend for (bstart, bend) in for_blocks)
                        if not in_for:
                            l = lines[k]
                            # Increment patterns: ++var, var++, var += 1, var = var + 1
                            if re.search(
                                    r'(\+\+' + re.escape(var) + r'|' + re.escape(var) + r'\+\+|' +
                                    re.escape(var) + r'\s*\+=\s*1\b|' +
                                    re.escape(var) + r'\s*=\s*' + re.escape(var) + r'\s*\+\s*1\b)',
                                    l):
                                inc_outside += 1
                            # Decrement patterns: --var, var--, var -= 1, var = var - 1
                            if re.search(r'(--' + re.escape(var) + r'|' + re.escape(var) + r'--|' +
                                         re.escape(var) + r'\s*-=\s*1\b|' +
                                         re.escape(var) + r'\s*=\s*' + re.escape(
                                var) + r'\s*-\s*1\b)', l):
                                dec_outside += 1
                        k += 1

                    # If both increment and decrement are found,
                    # record the line number of declaration/assignment (1-based)
                    if inc_outside and dec_outside:
                        result.append(i + 1)
                # Recursively analyze inner code blocks
                if '{' in line:
                    brace, block_start = 1, i
                    i += 1
                    while i <= end:
                        brace += lines[i].count("{")
                        brace -= lines[i].count("}")
                        if brace == 0:
                            analyze_block(block_start + 1, i - 1)
                            break
                        i += 1
                else:
                    i += 1

        # For each method, analyze its body
        for m_start, m_end in methods():
            analyze_block(m_start + 1, m_end)
        return sorted(result)

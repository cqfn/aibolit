# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from typing import List, Tuple

from javalang.ast import Node
from javalang.tree import CompilationUnit

from javalang.parse import parse

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class Lines:
    """
    Return the lines for some AST

    Deprecated: This class is used ony once by JavalangImproved
    and does not provide any complex functionality, so should be removed.
    """
    def __init__(self, filename: str | os.PathLike) -> None:
        self._filename = filename

    def value(self) -> Tuple[Node, List[str]]:
        source_code = read_text_with_autodetected_encoding(self._filename)

        lines = source_code.splitlines(keepends=True)
        tree: CompilationUnit = parse(source_code)

        return tree, lines

# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT
import os

from javalang.parse import parse
from javalang.tree import CompilationUnit

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


def build_ast(filename: str | os.PathLike) -> CompilationUnit:
    return parse(read_text_with_autodetected_encoding(filename))


def build_ast_from_string(content: str) -> CompilationUnit:
    return parse(content)

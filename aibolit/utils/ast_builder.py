from javalang.parse import parse
from javalang.tree import CompilationUnit

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


def build_ast(filename: str) -> CompilationUnit:
    return parse(read_text_with_autodetected_encoding(filename))

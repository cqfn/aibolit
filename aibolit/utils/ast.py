from javalang.parse import parse
from javalang.tree import CompilationUnit
import cchardet  # type: ignore


class AST:
    """
    Returns the AST for some java file
    """

    def __init__(self, filename: str):
        self._filename = filename
        self.encoding = 'utf-8'

    def value(self) -> CompilationUnit:
        with open(self._filename, 'rb') as file:
            bin_data = file.read()

        self.encoding = cchardet.detect(bin_data)['encoding']
        with open(self._filename, 'r', encoding=self.encoding) as file:  # type: ignore
            return parse(file.read())

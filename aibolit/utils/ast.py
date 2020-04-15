from javalang.parse import parse
from javalang.tree import CompilationUnit


class AST:
    """
    Returns the AST for some java file
    """

    def __init__(self, filename: str):
        self._filename = filename

    def value(self) -> CompilationUnit:
        """
        @todo #131:30min Introduce tests for AST.value method.
         Currently AST.value method is not being tested. It justs delegates a
         call to javalang library, but we should at least test which kinds of
         file this class should and which it should not support.
        """
        with open(self._filename, encoding='utf-8') as file:
            return parse(file.read())

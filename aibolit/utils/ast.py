import javalang


class Ast:
    """
    Returns the AST for some java file
    """

    def __init__(self, filename: str):
        self._filename = filename

    def value(self) -> javalang.ast.Node:
        with open(self._filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())
        return tree

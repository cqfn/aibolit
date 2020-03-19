import javalang.ast
import javalang.parse
import javalang.tree


_OP_EQUALITY = '=='
_LT_NULL = 'null'


class NullCheck(object):
    def value(self, filename: str):
        tree = self.__file_to_ast(filename)

        return self.__traverse_node(tree)

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """

        with open(filename) as file:
            return javalang.parse.parse(file.read())

    def __traverse_node(self, tree: javalang.ast.Node):
        lines = list()

        for path, node in tree.filter(javalang.tree.BinaryOperation):
            if _is_null_check(node):
                lines.append(node.operandr.position.line)

        return lines


def _is_null_check(node: javalang.ast.Node):
    return node.operator == _OP_EQUALITY and node.operandr.value == _LT_NULL

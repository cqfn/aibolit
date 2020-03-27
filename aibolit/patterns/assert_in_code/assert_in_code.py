import javalang.ast
import javalang.parse
import javalang.tree


_TEST_CLASS_SUFFIX = 'Test'


class AssertInCode(object):
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

        for path, node in tree.filter(javalang.tree.AssertStatement):
            if not _within_test_class(path):
                # HACK: Neither `assert` statement nor its condition doesn't have
                # a position, so we only could take it from the left operand.
                #
                # SEE: https://github.com/c2nes/javalang/issues/73
                lines.append(node.condition.operandl.position.line)

        return lines


def _within_test_class(path) -> bool:
    class_declaration = next(filter(_is_class_declaration, path[::2]))

    return class_declaration.name.endswith(_TEST_CLASS_SUFFIX)


def _is_class_declaration(node: javalang.ast.Node) -> bool:
    return isinstance(node, javalang.tree.ClassDeclaration)

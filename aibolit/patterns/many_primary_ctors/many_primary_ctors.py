import javalang.ast
import javalang.parse
import javalang.tree


class ManyPrimaryCtors(object):
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

        for _, class_declaration in tree.filter(javalang.tree.ClassDeclaration):
            primary_ctors = list(filter(_is_primary, class_declaration.constructors))

            if len(primary_ctors) > 1:
                lines.extend(ctor.position.line for ctor in primary_ctors)

        return lines


def _is_primary(constructor: javalang.tree.ConstructorDeclaration):
    for _, assignment in constructor.filter(javalang.tree.Assignment):
        if _is_instance_variable_assignment(assignment):
            return True

    return False


def _is_instance_variable_assignment(assignment: javalang.tree.Assignment):
    return isinstance(assignment.expressionl, javalang.tree.This)

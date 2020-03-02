import javalang


class InstanceOf:

    def __init__(self):
        pass

    def __traverse_node(self, node):
        """
        Travers over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        lines = []
        for path, node_elem in node.filter(javalang.tree.BinaryOperation):
            if node_elem.operator == 'instanceof':
                code_line = node_elem.operandl.position.line or node_elem.operandr.position.line
                lines.append(code_line)
        for path, node_elem in node.filter(javalang.tree.MethodInvocation):
            if node_elem.member == 'isInstance':
                lines.append(node_elem.position.line)

        return lines

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = javalang.parse.parse(file.read())
        return res

    # flake8: noqa: C901
    def value(self, filename: str):
        tree = self.__file_to_ast(filename)
        return self.__traverse_node(tree)

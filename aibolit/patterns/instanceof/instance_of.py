import javalang
from aibolit.utils.ast import AST


class InstanceOf:
    def __init__(self):
        pass

    def __traverse_node(self, node):
        """
        Traverse over AST tree finds instance_of and .isInstance().
        :param filename:
        :return:
        List of code lines
        """
        lines = []
        for path, node_elem in node.filter(javalang.tree.BinaryOperation):
            if node_elem.operator == 'instanceof' and node_elem.operandl.position is not None:
                code_line = node_elem.operandl.position.line or node_elem.operandr.position.line
                lines.append(code_line)
        for path, node_elem in node.filter(javalang.tree.MethodInvocation):
            if node_elem.member == 'isInstance':
                lines.append(node_elem.position.line)

        return lines

    def value(self, filename: str):
        tree = AST(filename).value()
        return self.__traverse_node(tree)

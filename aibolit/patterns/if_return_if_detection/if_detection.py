import javalang
from aibolit.patterns.var_middle.var_middle import ASTNode, JavalangImproved


class newJavalangImproved(JavalangImproved):

    def __tree_to_nodes(self, tree, line=1, parent_method_line=None):
        '''Return AST nodes with line numbers sorted by line number'''

        if hasattr(tree, 'position') and tree.position:
            line = tree.position.line

        line = self.__fix_line_number_if_possible(tree, line)
        if type(tree) == (javalang.tree.IfStatement or javalang.tree.BlockStatement):
            parent_method_line = line

        res = []
        for child in tree.children:
            nodes_arr = child if isinstance(child, list) else [child]
            for node in nodes_arr:
                if not hasattr(node, 'children'):
                    continue
                left_siblings_line = res[-1].line if len(res) > 0 else line
                res += self.__tree_to_nodes(
                    node,
                    left_siblings_line,
                    parent_method_line
                )

        return [ASTNode(line, parent_method_line, tree)] + res

    def filter(self, ntypes):
        nodes = self.tree_to_nodes()
        array = []
        for index, i in enumerate(nodes):
            if (type(i.node) in ntypes):
                if type(i.node.then_statement) in [javalang.tree.BlockStatement] and i.node.else_statement is not None:
                    for check_return in i.node.then_statement.statements:
                        if type(check_return) in [javalang.tree.ReturnStatement]:
                            array.append(nodes[index].line + 1)
        return array


class CountIfReturn:
    '''
    Returns lines in the file where exist if statement with return inside and else statement
    '''
    def __init__(self):
        pass

    def value(self, filename: str):
        ''''''
        tree = newJavalangImproved(filename)
        if_decls = tree.filter([javalang.tree.IfStatement])

        return if_decls

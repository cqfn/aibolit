import javalang
from aibolit.patterns.var_middle.var_middle import JavalangImproved


class newJavalangImproved(JavalangImproved):

    def filter(self, ntypes):
        nodes = self.tree_to_nodes()
        array = []
        for index, i in enumerate(nodes):
            if (type(i.node) in ntypes):
                if type(i.node.then_statement) in [javalang.tree.BlockStatement] and i.node.else_statement is not None:
                    for check_return in i.node.then_statement.statements:
                        if type(check_return) in [javalang.tree.ReturnStatement]:
                            array.append(nodes[index].line)
        return array


class CountIfReturn:
    '''
    Returns lines with if statement which has also return statement
    and other conditions with else.
    '''
    def __init__(self):
        pass

    def value(self, filename: str):
        ''''''
        tree = newJavalangImproved(filename)
        if_decls = tree.filter([javalang.tree.IfStatement])

        return if_decls

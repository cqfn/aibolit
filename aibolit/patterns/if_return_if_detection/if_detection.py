import javalang


# mapping between javalang node class names and Java keywords
NODE_KEYWORD_MAP = {
    'SuperMethodInvocation': 'super',
    'WhileStatement': 'while',
    'ForStatement': 'for',
    'TryStatement': 'try',
    'CatchClause': 'catch',
}


class ASTNode:

    def __init__(self, line, method_line, node):
        self.line = line  # node line number in the file
        self.method_line = method_line  # line number where parent method declared
        self.node = node  # javalang AST node object


class JavalangImproved:

    def __init__(self, filename: str):
        tree, lines = self.__file_to_ast(filename)
        self.tree = tree
        self.lines = lines

    def __file_to_ast(self, filename: str):
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        with open(filename, encoding='utf-8') as file:
            lines = file.readlines()
        return tree, lines

    def __find_keyword(self, lines, keyword, start):
        for i in range(start - 1, len(lines)):
            if keyword in lines[i]:
                return i + 1
        return -1

    def __fix_line_number_if_possible(self, node: javalang.ast.Node, line_n):
        node_class_name = node.__class__.__name__
        if node_class_name not in NODE_KEYWORD_MAP:
            return line_n
        line = self.__find_keyword(
            self.lines,
            NODE_KEYWORD_MAP[node_class_name],
            line_n
        )
        if line == -1:
            return line_n
        return line

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

    def tree_to_nodes(self):
        '''Return AST nodes as list with line numbers sorted by line number'''
        nodes = self.__tree_to_nodes(self.tree)
        return sorted(nodes, key=lambda v: v.line)

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
    Returns lines with if statement which has also returb statement and other conditions with else.
    '''
    def __init__(self):
        pass

    def value(self, filename: str):
        ''''''
        tree = JavalangImproved(filename)
        if_decls = tree.filter([javalang.tree.IfStatement])

        return if_decls

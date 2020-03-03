import javalang

class ForceTypeCastingFinder:
    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        '''Takes path to java class file and returns AST Tree'''
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree
    def __process_node(self, node):
        line = node.position.line if hasattr(node, 'position') and node.position is not None else None
        qualifier = node.qualifier if hasattr(node, 'qualifier') else None
        member = node.member if hasattr(node, 'member') else None
        name = node.name if hasattr(node, 'name') else None
        return {
            "line": line,
            "name": qualifier or member or name,
            "ntype": type(node)
        }

    def __tree_to_list(self, tree: javalang.tree.CompilationUnit):
        '''Convert AST tree to list of object'''
        items = [self.__process_node(node) for path, node in tree if node is not None]

        # fill missed line numbers
        last_line_number = None

        for item in items:
            if (item['line']) is not None:
                last_line_number = item['line']
                continue
            item['line'] = last_line_number

        return items
    def value(self, filename: str):
        ''''''
        tree = self.__file_to_ast(filename)
        list_tree = self.__tree_to_list(tree)
        num_str = []
        for node in list_tree:
            if node['ntype'] == javalang.tree.Cast:
                k = int(node['line'])
                if k not in num_str:
                    num_str.append(k)
        return num_str

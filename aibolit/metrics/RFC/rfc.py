from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage
from typing import Set, Any


class RFC:
    '''
    The Response For a Class is an object-oriented
    metric that shows the interaction of the class'
    methods with other methods.
    '''
    def __init__(self):
        self.class_methods = {}

    def exclude_inhereted_methods(self) -> Set[Any]:
        temp = self.class_methods.copy()
        for each_method in self.class_methods.keys():
            counter = 0
            for i in self.class_methods[each_method]:
                if i in self.class_methods:
                    counter += 1
                else:
                    counter -= 1
            if counter > 0:
                temp.pop(each_method)
        final_rfc = set()
        for declared_method in temp.keys():
            if len(declared_method) != 0:
                final_rfc.add(declared_method)

        for invoked_methods in temp.values():
            for each_method in invoked_methods:
                final_rfc.add(each_method)
        return final_rfc

    def get_invoked(self, tree) -> Set[Any]:
        inv_names = set()
        inv_methods = tree.nodes_by_type(ASTNodeType.METHOD_INVOCATION)
        for inv_method in inv_methods:
            name_of_invoked_class = tree.get_method_invocation_params(inv_method)
            current_name = name_of_invoked_class.method_name
            inv_names.add(current_name)
        return inv_names

    def value(self, filename: str) -> int:  # noqa: C901
        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            declareted_methods = tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION)
            for class_method in declareted_methods:
                ast_each_method = AST(tree.tree.subgraph(class_method), class_method[0])
                # to form a set of all methods in the class
                names = list(ast_each_method.children_with_type(ast_each_method.root, ASTNodeType.STRING))
                for each_string in names:
                    method_name = tree.get_attr(each_string, 'string')
                    # we need to check the name because even comments are counted as the childs with string type
                    # need to get rid of them
                    if not method_name.startswith('/'):
                        self.class_methods[method_name] = set()
                        break

            # to count invoked methods
            tree = p.java_classes[class_name]
            declareted_methods = tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION)
            for meth_name, class_method in zip(self.class_methods.keys(), declareted_methods):
                ast_each_method = AST(tree.tree.subgraph(class_method), class_method[0])
                invoked_names = self.get_invoked(ast_each_method)
                for i in invoked_names:
                    self.class_methods[meth_name].add(i)

        final_rfc = len(self.exclude_inhereted_methods())
        self.class_methods.clear()
        return final_rfc

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_package import JavaPackage


class RFC:
    '''
    The Response For a Class is an object-oriented
    metric that shows the interaction of the class'
    methods with other methods.
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> int:
        class_methods = set()
        called_methods = set()
        initialized_method_vars = set()

        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            for class_method in tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION):
                ast_each_method = AST(tree.tree.subgraph(class_method), class_method[0])
                # to form a set of all methods in the class
                names = list(ast_each_method.children_with_type(ast_each_method.root, ASTNodeType.STRING))
                for each_string in names:
                    method_name = tree.get_attr(each_string, 'string')
                    # we need to check the name because even comments are counted as the childs with string type
                    # need to get rid of them
                    if not method_name.startswith('/'):
                        class_methods.add(method_name)
                        break

                for new_method_var in ast_each_method.nodes_by_type(ASTNodeType.VARIABLE_DECLARATOR):
                    for inv_method in ast_each_method.children_with_type(new_method_var, ASTNodeType.METHOD_INVOCATION):
                        new_var_list = list(ast_each_method.children_with_type(new_method_var, ASTNodeType.STRING))
                        new_var = ast_each_method.get_attr(new_var_list[0], 'string')
                        initialized_method_vars.add(new_var)

                        name_of_invoked_class = ast_each_method.get_method_invocation_params(inv_method)
                        current_name = name_of_invoked_class.method_name
                        if not current_name.startswith('/'):
                            if current_name not in initialized_method_vars:
                                called_methods.add(current_name)

                # to count invoked methods without initialization the results into new variable
                for inv_method in ast_each_method.nodes_by_type(ASTNodeType.METHOD_INVOCATION):
                    name_of_invoked_class = ast_each_method.get_method_invocation_params(inv_method)
                    current_name = name_of_invoked_class.method_name
                    if current_name not in initialized_method_vars:
                        called_methods.add(current_name)

        return len(class_methods.union(called_methods))

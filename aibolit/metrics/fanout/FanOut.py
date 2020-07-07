from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from itertools import islice
from aibolit.ast_framework.java_package import JavaPackage


class FanOut:
    '''
    Fan Out metric is defined as the number of other classes referenced by a class.
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> int:  # noqa: C901

        # exception are used from https://checkstyle.sourceforge.io/config_metrics.html#ClassFanOutComplexity
        considered_classes = {'ArrayIndexOutOfBoundsException': 0, 'ArrayList': 0, 'Boolean': 0, 'Byte': 0,
                              'Character': 0, 'Class': 0, 'Deprecated': 0, 'Deque': 0, 'Double': 0,
                              'Exception': 0, 'Float': 0, 'FunctionalInterface': 0, 'HashMap': 0,
                              'HashSet': 0, 'IllegalArgumentException': 0, 'IllegalStateException': 0,
                              'IndexOutOfBoundsException': 0, 'Integer': 0, 'LinkedList': 0, 'List': 0,
                              'Long': 0, 'Map': 0, 'NullPointerException': 0, 'Object': 0, 'Override': 0,
                              'Queue': 0, 'RuntimeException': 0, 'SafeVarargs': 0, 'SecurityException': 0,
                              'Set': 0, 'Short': 0, 'SortedMap': 0, 'SortedSet': 0, 'String': 0, 'StringBuffer': 0,
                              'StringBuilder': 0, 'SuppressWarnings': 0, 'Throwable': 0, 'short': 0, 'void': 0,
                              'TreeMap': 0, 'TreeSet': 0, 'UnsupportedOperationException': 0, 'Void': 0,
                              'System.out': 0, 'boolean': 0, 'byte': 0, 'char': 0, 'double': 0, 'float': 0,
                              'int': 0, 'long': 0,
                              }
        fan_outs = 0

        # check imported classes
        tree = AST.build_from_javalang(build_ast(filename))
        for each_import in (tree.children_with_type(tree.root, ASTNodeType.IMPORT)):
            name_node, = islice(tree.children_with_type(each_import, ASTNodeType.STRING), 1)
            new_class = tree.get_attr(name_node, 'string').split('.')[-1]
            if considered_classes.get(new_class) is None:
                fan_outs += 1
                considered_classes[new_class] = 0

        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            for var_node in tree.get_nodes(ASTNodeType.VARIABLE_DECLARATOR):
                var_child = list(tree.children_with_type(var_node, ASTNodeType.STRING))
                new_class_name = tree.get_attr(var_child[0], 'string')

                for class_creator_node in tree.children_with_type(var_node, ASTNodeType.CLASS_CREATOR):
                    for go_to_name in tree.children_with_type(class_creator_node, ASTNodeType.REFERENCE_TYPE):
                        classC_child = list(tree.children_with_type(go_to_name, ASTNodeType.STRING))
                        used_class_name = tree.get_attr(classC_child[0], 'string')
                        if considered_classes.get(used_class_name) is None:
                            considered_classes[used_class_name] = 0
                            fan_outs += 1
                        if considered_classes.get(new_class_name) is None:
                            considered_classes[new_class_name] = 0

        # check classes of invokated methods
        for i in tree.get_nodes(ASTNodeType.STATEMENT_EXPRESSION):
            for invoked_method_child in tree.children_with_type(i, ASTNodeType.METHOD_INVOCATION):
                name_of_invoked_class = tree.get_method_invocation_params(invoked_method_child)
                if considered_classes.get(name_of_invoked_class.object_name) is None:
                    considered_classes[name_of_invoked_class.object_name] = 0
                    fan_outs += 1

        return fan_outs

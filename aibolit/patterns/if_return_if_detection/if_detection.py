from aibolit.utils.ast import ASTNodeType
from aibolit.utils.java_package import JavaPackage
from typing import List


class CountIfReturn:
    '''
    Returns lines with if statement which has also return statement
    and other conditions with else.
    '''
    def __init__(self):
        pass

    def value(self, filename: str) -> List[int]:
        detected_lines = []
        p = JavaPackage(filename)
        for class_name in p.java_classes:
            tree = p.java_classes[class_name]
            for index, each_object in enumerate(tree.nodes_by_type(ASTNodeType.IF_STATEMENT)):
                all_childs = list([i for i in tree.tree.succ[each_object]])
                if len(all_childs) == 3:
                    for i in tree.tree.succ[all_childs[1]]:
                        if tree.get_type(i) == ASTNodeType.RETURN_STATEMENT:
                            detected_lines += [tree.get_attr(each_object, 'source_code_line')]
        return detected_lines

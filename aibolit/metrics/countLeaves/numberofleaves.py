import javalang
from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType

from typing import Dict, List, Type, Any
from collections import OrderedDict


class CountNumberOfLeaves:
    '''
    Returns number of leaves in class (sum by each method).
    input: file_path
    output: sum of leaves in class by each method
    '''
    def countLeaves(self, root: Type) -> int:
        # forming the same data type for each object
        root_arr = root if isinstance(root, List) else [root]
        leaves = 0
        not_count: List[Any] = [None, '', set()]

        # traverse through all childs of object. If there is no child, hence we faced leaf
        for node in root_arr:

            if not hasattr(node, 'children') and node not in not_count:
                return leaves + 1

            elif node in not_count:
                continue

            for each_child in node.children:
                leaves += self.countLeaves(each_child)

        return leaves

    def value(self, filename: str) -> int:

        tree = build_ast(filename)
        traversed = []
        for _, class_body in tree.filter(javalang.tree.ClassDeclaration):
            for each_object in class_body.body:
                if isinstance(each_object, javalang.tree.MethodDeclaration):
                    traversed.append(self.countLeaves(each_object.body))

        return sum(traversed)
    
    
    def countLeaves_probing(self, node: ASTNodeType) -> int:
        leaves = 0
        if not len(list(node.children)):
            return leaves + 1
        
        for each_child in node.children:
            leaves += self.countLeaves_probing(each_child)
        return leaves

    def probing_values(self, ast: AST) -> Dict[str, int]:
        """
        Number of leaves for each method
        """
        values_dict = OrderedDict()
        for method_ast in ast.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method_name = method_ast.get_root().name
            start_line = method_ast.get_root().line
            
            method_value = self.countLeaves_probing(method_ast.get_root())
            values_dict[f"{method_name}:{start_line}"] = method_value
        return values_dict

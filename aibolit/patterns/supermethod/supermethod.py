from aibolit.ast_framework.ast import AST, ASTNodeType
from aibolit.ast_framework.java_package import JavaPackage
from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding
import re
from typing import List


class SuperMethod:

    def __init__(self):
        pass

    def _get_node_name(self, ast: AST, node: int) -> str:
        extracted_name = None
        names = ast.children_with_type(node, ASTNodeType.STRING)
        for each_string in names:
            method_name = ast.get_attr(each_string, 'string')
            # Checking not to start with '/' is aimed to get
            # rid of comments, which are all childs of node.
            # We check the occurance any letter in name in order
            # to get rid of '' string and None.
            if not method_name.startswith('/') and re.search(r'[^\W\d]', method_name) is not None:
                extracted_name = method_name
                return extracted_name
        return ''

    def value(self, filename: str) -> List[int]:
        """
        Iterates over functions and finds super.func() calls.
        Javalang doesn't have code line for super.func() call,
        that's why we can only count the first match of a call inside some function.
        It has MULTIPLE MATCHES if we call super.func() inside a ANONYMOUS CLASS.
        :param filename:
        :return: Lines of code
        """
        results = []
        source_code = read_text_with_autodetected_encoding(filename)
        lines = source_code.splitlines()
        tree = JavaPackage(filename)
        for method_decl_node in tree.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION):
            ast = AST(tree.tree.subgraph(method_decl_node), method_decl_node[0])
            code_line = ast.get_attr(method_decl_node[0], 'source_code_line')
            for super_method_inv in ast.nodes_by_type(ASTNodeType.SUPER_METHOD_INVOCATION):
                str_to_find = 'super.{method_name}('.format(
                    method_name=self._get_node_name(ast, super_method_inv)).strip()
                for iter, line in enumerate(lines[code_line - 1:]):
                    string_strip = line.strip().replace('\t', '')
                    if string_strip.find(str_to_find) > -1:
                        results.append(code_line + iter)
                        break
        return results

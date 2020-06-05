from javalang.parse import parse
from javalang.tree import MethodDeclaration, SuperMethodInvocation

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding


class SuperMethod:

    def __init__(self):
        pass

    def value(self, filename: str):
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
        tree = parse(source_code)
        lines = source_code.splitlines()
        for _, method_decl_node in tree.filter(MethodDeclaration):
            code_line = method_decl_node.position.line
            for _, super_method_inv in method_decl_node.filter(SuperMethodInvocation):
                str_to_find = 'super.{method_name}('.format(
                    method_name=super_method_inv.member).strip()
                for iter, line in enumerate(lines[code_line - 1:]):
                    string_strip = line.strip().replace('\t', '')
                    if string_strip.find(str_to_find) > -1:
                        results.append(code_line + iter)
                        break
        return results

    def __traverse(self, tree, results):
        descendants = tree.children
        for children in descendants:
            if isinstance(children, tuple) or isinstance(children, list):
                for item in children:
                    if isinstance(item, SuperMethodInvocation):
                        results.append([item.member])
                    else:
                        self.__traverse(item, results)
        return results

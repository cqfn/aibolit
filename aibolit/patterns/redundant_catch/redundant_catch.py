import itertools
import re
from collections import namedtuple

import javalang

ExceptionInfo = namedtuple('ExceptionInfo', 'func_name, catch_list, throws_list, line_number')


class RedundantCatch:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        """
        with open(filename, encoding='utf-8') as file:
            tree = javalang.parse.parse(file.read())

        return tree

    def value(self, filename):
        tree = self.__file_to_ast(filename)
        with open(filename, encoding='utf-8') as file:
            lines_str = file.readlines()

        pattern_catch = re.compile(r'(catch[\(\s]+[\w | \s]+)')
        total_code_lines = []
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            catch_list = []
            ei = ExceptionInfo(
                func_name=method_node.name,
                catch_list=catch_list,
                throws_list=method_node.throws,
                line_number=method_node.position.line
            )
            for _, try_node in method_node.filter(javalang.tree.TryStatement):
                catch_classes = [x.parameter.types for x in try_node.catches]
                classes_exception_list = list(itertools.chain(*catch_classes))
                ei.catch_list.extend(classes_exception_list)
                catches = [
                    (i, line) for i, line in
                    enumerate(lines_str[method_node.position.line:], start=method_node.position.line)
                    if re.search(pattern_catch, line)
                ]
                code_lines = [
                    i + 1 for i, line in catches
                    if any([(line.find(y) > -1) for y in ei.throws_list])
                ]
                total_code_lines.extend(code_lines)
                # print(method_node.name, try_node.catches)
            # print(total_code_lines)

        return sorted(set(total_code_lines))

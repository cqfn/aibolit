import javalang
import re
from aibolit.utils.utils import RemoveComments


class StringConcatFinder:

    def __init__(self):
        pass

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = RemoveComments.remove_comments(file.read())

        return res

    def value(self, filename: str):
        text = self.__file_to_ast(filename)
        pattern_without_quote_first = re.compile(r'(?<=([\w])\+)\"[\w]+\"')
        pattern_with_quote_first = re.compile(r'(?<=([\w]\")\+)[\w]+')
        lines = []
        for iter, line in enumerate(text.splitlines()):
            t_str = line.replace(' ', '')
            if re.search(pattern_without_quote_first, t_str) \
                    or re.search(pattern_with_quote_first, t_str):
                lines.append(iter)
        return lines

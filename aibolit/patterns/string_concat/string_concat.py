import javalang
import re
from aibolit.utils.utils import RemoveComments


class StringConcatFinder:

    def __init__(self):
        pass

    """
        @todo #131:30min NoComments implementation of Ast
         this __file_to_ast implementation differs from usual ones since it 
         removes the comments from it. Implement a decorator to Ast which does 
         it and replace it here. Don't forget the tests.
    """
    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            text = file.read()
            lines_map = {line: i for i, line in enumerate(text.splitlines(), start=1)}
            res = RemoveComments.remove_comments(text)

        return res, lines_map

    def value(self, filename: str):
        text, split_text = self.__file_to_ast(filename)
        pattern_without_quote_first = re.compile(r'(?<=([\w])\+)\"[\w]+\"')
        pattern_with_quote_first = re.compile(r'(?<=([\w]\")\+)[\w]+')
        lines = []
        for line in text.splitlines():
            t_str = line.replace(' ', '')
            if re.search(pattern_without_quote_first, t_str) \
                    or re.search(pattern_with_quote_first, t_str):
                code_line = split_text[line]
                lines.append(code_line)
        return lines

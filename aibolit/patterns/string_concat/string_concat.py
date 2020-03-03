import javalang
import re


class StringConcatFinder:

    def __init__(self):
        pass

    def remove_comments(self, string):
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "",
                        string)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        string = re.sub(re.compile(r"//.*?\n"), "",
                        string)
        return string

    def __file_to_ast(self, filename: str) -> javalang.ast.Node:
        """
        Takes path to java class file and returns AST Tree
        :param filename:
        :return: Tree
        """
        with open(filename, encoding='utf-8') as file:
            res = self.remove_comments(file.read())

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

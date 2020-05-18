from typing import List
from aibolit.types_decl import LineNumber


class NonFinalArgument:
    def __init__(self):
        pass

    def value(self, filename: str) -> List[LineNumber]:
        """
        Returns the line numbers of the file name which contains no final arguments
        :param filename: name of the file
        :return: number of the lines with non-final arguments
        @todo #146:30min Implement NonFinalArgument pattern.
         All method arguments must have final modifiers. Once we find an argument
         without final, it's a pattern. After implementing that, enable tests in
         test_non_final_argument.py
        """
        return []

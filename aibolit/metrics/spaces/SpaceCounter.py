# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List
from statistics import variance

from aibolit.utils.encoding_detector import read_text_with_autodetected_encoding
from aibolit.utils.utils import RemoveComments


class IndentationCounter:

    def __init__(
        self,
        left_var: bool = False,
        right_var: bool = False,
        max_left: bool = False,
        max_right: bool = False
    ) -> None:
        self.left_var = left_var
        self.right_var = right_var
        self.max_left = max_left
        self.max_right = max_right

    def __file_to_tokens(self, filename: str) -> List[str]:
        """
        Takes path to java class file and returns tokens

        :param filename: file name
        :return: list of counted spaces
        """
        source_code = read_text_with_autodetected_encoding(filename)
        source_code = RemoveComments.remove_comments(source_code)
        return [line.replace('\t', '    ') for line in source_code.splitlines()
                if line]

    def value(self, filename: str) -> float | None:
        lines = self.__file_to_tokens(filename)
        if not lines or len(lines) == 1:
            return 0

        spaces_per_line = []
        prev_left = 0
        prev_right = len(lines[0])
        for i, line in enumerate(lines):
            first_non_space_symbol_pos = len(line) - len(line.lstrip(' '))
            spaces_per_line.append(
                [i,
                 # count the difference between the position of first symbol in cur string and
                 # the position of first symbol of previous string
                 first_non_space_symbol_pos - prev_left,
                 # count the difference between the position of last symbol in cur string and
                 # the position of last symbol of previous string
                 len(line) - prev_right
                 ])
            prev_left = first_non_space_symbol_pos
            prev_right = len(line)

        val = None
        if self.left_var:
            val = variance([x[1] for x in spaces_per_line])
        elif self.right_var:
            val = variance([x[2] for x in spaces_per_line])
        elif self.max_left:
            val = max([abs(x[1]) for x in spaces_per_line])
        elif self.max_right:
            val = max([abs(x[2]) for x in spaces_per_line])

        return val

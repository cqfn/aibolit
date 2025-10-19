# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import re


class RemoveComments:

    def __init__(self) -> None:
        pass

    @staticmethod
    def remove_comments(string: str) -> str:
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile(r'/\*.*?\*/', re.DOTALL), '',
                        string)
        # remove all occurrence single-line comments (//COMMENT\n ) from string
        string = re.sub(re.compile(r'//.*?\n'), '',
                        string)
        return string

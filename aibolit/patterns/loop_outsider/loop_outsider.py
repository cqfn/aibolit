# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
from typing import List
from aibolit.types_decl import LineNumber


class LoopOutsider:
    """
    Pattern which matches loop outsiders: when we modify a variable which is declared outside of the
    scope of the loop.
    """

    def __init__(self):
        pass

    def value(self, filename) -> List[LineNumber]:
        """
        Returns the line number of loop outsiders found in file.
        """
        return []

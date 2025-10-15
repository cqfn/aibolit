# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT
import os
from typing import List


class BidirectIndex:

    def __init__(self) -> None:
        pass

    def value(self, filename: str | os.PathLike) -> List[int]:
        """
        Finds if a variable is being incremented and decremented within the same method

        :param filename: filename to be analyzed
        :return: list of LineNumber with the variable declaration lines

        @todo #139:30min Implement bidirect index pattern
        If the same numeric variable is incremented and decremented within the same method,
        it's a pattern. A numeric variable should either be always growing or decreasing.
        Bi-directional index is confusing. The method must return a list with the line numbers
        of the variables that match this pattern. After implementation, activate tests in
        test_bidirect_index.py
        """
        return []

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import Union
import os


class Loc:
    def __init__(self, path: Union[str, os.PathLike]) -> None:
        self.path = path

    def value(self) -> int:
        with open(self.path, encoding='utf-8') as buf:
            return sum(1 for line in buf)

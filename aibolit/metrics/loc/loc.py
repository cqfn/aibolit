# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


class Loc:
    def __init__(self, path):
        self.path = path

    def value(self):
        line_number = -1
        with open(self.path, encoding='utf-8') as f:
            for idx, _ in enumerate(f):
                line_number = idx
        return line_number + 1

# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT


class Loc:
    def __init__(self, path):
        self.path = path

    def value(self):
        with open(self.path, encoding='utf-8') as buf:
            return sum(1 for line in buf)

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT


class Loc:
    def __init__(self, path):
        self.path = path

    def value(self):
        i = -1
        with open(self.path, encoding='utf-8') as f:
            for i, l in enumerate(f):
                pass
        return i + 1

# SPDX-FileCopyrightText: Copyright (c) 2020 Aibolit
# SPDX-License-Identifier: MIT


class Loc:
    def __init__(self, path):
        self.path = path

    def value(self):
        with open(self.path) as f:
            for i, l in enumerate(f):
                pass
            return i + 1

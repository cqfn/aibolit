# SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
# SPDX-License-Identifier: MIT


class Loc:
    def __init__(self, path):
        self.path = path

    def value(self):
        with open(self.path) as f:
            for i, l in enumerate(f):
                pass
            return i + 1

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class JoinedValidationOrAnd {
    void print(int x, int y) {
        if (x == 1 || y == 1 && a == 1) {
            throw new Exception("Oops");
        }
    }
}

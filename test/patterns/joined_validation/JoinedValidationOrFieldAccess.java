// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class JoinedValidationAndOr {

    int field = 0;

    void print(int x, int y) {
        if (x == 1 || this.field == 1) {
            throw new Exception("Oops");
        }
    }
}

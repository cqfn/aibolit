// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class SimpleJoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y == 1) { // here!
            throw new Exception("Oops");
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class SimpleJoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y == 1) { // here!
            throw new Exception("Oops");
        }
    }
}

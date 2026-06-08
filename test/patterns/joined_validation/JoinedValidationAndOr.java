// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class JoinedValidationAndOr {
    void print(int x, int y) {
        if (a == 1 && x == 1 || y == 1) {
            throw new Exception("Oops");
        }
    }
}

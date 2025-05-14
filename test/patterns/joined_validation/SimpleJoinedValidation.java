// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

class SimpleJoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y == 1) { // here!
            throw new Exception("Oops");
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class MutableIndexHiddenNestedFor {
    void mutableIndexHiddenNestedFor() {
        for (int i = 1; i < 5; ++i ) {
            for (int i = 1; i < 5; ++i ) {
                i  = i + 1; // what cycle is changing a variable?
            }
        }
    }
}

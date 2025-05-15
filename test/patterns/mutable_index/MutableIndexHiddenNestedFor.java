// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

class MutableIndexHiddenNestedFor {
    void mutableIndexHiddenNestedFor() {
        for (i = 1; i < 5; ++i ) {
            for (i = 1; i < 5; ++i ) {
                i  = i + 1; // what cycle is changing a variable?
            }
        }
    }
}

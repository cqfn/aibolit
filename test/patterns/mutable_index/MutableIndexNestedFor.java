// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

class MutableIndexNestedFor {
    void mutableIndexNestedFor() {
        for (i = 1; i < 5; ++i ) {
            for (j = 1; j < 5; ++j) {
                i++;
            }
        }
    }
}

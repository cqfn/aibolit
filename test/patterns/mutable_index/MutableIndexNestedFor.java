// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
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

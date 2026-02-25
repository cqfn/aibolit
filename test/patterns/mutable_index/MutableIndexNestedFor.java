// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class MutableIndexNestedFor {
    void mutableIndexNestedFor() {
        for (int i = 1; i < 5; ++i ) {
            for (int j = 1; j < 5; ++j) {
                i++;
            }
        }
    }
}

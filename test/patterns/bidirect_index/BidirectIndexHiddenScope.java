// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class BidirectIndexHiddenScope {
    void bidirectIndexHiddenScopeTrue() {
        i = 0;
        for (int i=0; i < 10; i++) {
            ++i; // fake case
        }
        --i; // fake case
    }
    void bidirectIndexHiddenScopeFalse() {
        i = 0;
        while(true) {
            int i = 0; // fake case
            ++i;
        }
        --i; //fake case
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class LoopOutsiderPrefixDecrementInWhile {
    public void loopOutsiderPrefixDecrementInWhile() {
        int x = 0;
        while (true) {
            x--; // here
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class LoopOutsiderPrefixIncrementInWhile {
    public void loopOutsiderPrefixIncrementInWhile() {
        int x = 0;
        while (true) {
            x++; // here
        }
    }
}

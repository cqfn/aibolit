// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class LoopOutsiderBiwiseInclusiveOrAndInWhile {
    public void loopOutsiderBiwiseInclusiveOrAndInWhile() {
        int x = 0;
        while (true) {
            x |= 1; // here
        }
    }
}

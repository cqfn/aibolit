// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class LoopOutsiderModulusAndInWhile {
    public void loopOutsiderModulusAndInWhile() {
        int x = 0;
        while (true) {
            x %= 1; // here
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class LoopOutsiderAssignmentInWhile {
    public void loopOutsiderAssignmentInWhile() {
        int x = 0;
        while (true) {
            x = 70; // here
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

public class LoopOutsiderBitwiseAndInWhile {
    public void loopOutsiderBitwiseAndInWhile() {
        int x = 0;
        while (true) {
            x &= 1; // here
        }
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class LoopOutsiderLeftShiftAndInWhile {
    public void loopOutsiderLeftShiftAndInWhile() {
        int x = 0;
        while (true) {
            x <<= 1; // here
        }
    }
}

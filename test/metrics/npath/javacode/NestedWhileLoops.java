// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
public class Test {
    public void nestedLoops() {
        int i = 0;
        while (i < 3) {
            int j = 0;
            while (j < 2) {
                j++;
            }
            i++;
        }
    }
}
// 3

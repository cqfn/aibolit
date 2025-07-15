// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
class Test {
    void search(int[] arr, int target) {
        for (int x : arr) {
            if (x == target) {
                break;
            }
            if (x < 0) {
                continue;
            }
            System.out.println(x);
        }
    }
}
// 5

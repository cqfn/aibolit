// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
class Test {
    void process(int[] data) {
        for (int x : data) {
            switch (x) {
                case 1: System.out.println("1");
                case 2: System.out.println("2");
                case 3: System.out.println("3");
                default: break;
            }
        }
    }
}
// 5

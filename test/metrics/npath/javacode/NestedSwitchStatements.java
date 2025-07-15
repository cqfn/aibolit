// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
class NestedSwitchStatements {
    public void process(int x, int y) {
        switch (x) { // 1 path through case and 4 - default
            case 1:
                System.out.println("X=1");
                break;
            default:
                switch (y) {
                    case 1: System.out.println("Y=1"); break;
                    case 2: System.out.println("Y=2"); break;
                    case 3: System.out.println("Y=3"); break;
                    default: System.out.println("Y=default"); break;
                }
        }
    }
}
// 5

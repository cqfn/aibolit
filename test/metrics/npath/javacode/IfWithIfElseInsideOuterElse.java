// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
class WithOneIfWithIfElseInElseClause {
    public void print(bool flag, bool ok) {
        if (flag) {
            System.out.println("Flag is true");
        } else {
            if (ok) {
                System.out.println("OK");
            } else {
                System.out.println("Not OK");
            }
        }
    }
}
// 3

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
class ComplexIfElse {
    public void checkValues(int a, int b) {
        if (a > 0) {
            if (b > 0) {
                System.out.println("Both a and b are greater than 0");
            } else {
                System.out.println("a is greater than 0, but b is not");
            }
        } else {
            if (b > 0) {
                System.out.println("a is not greater than 0, but b is");
            } else {
                System.out.println("Neither a nor b is greater than 0");
            }
        }
    }
}
// 4

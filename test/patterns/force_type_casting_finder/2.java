// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.lang.Math;

class T2 {
    public int square (int n) {
        return (int) java.lang.Math.pow(n,2);
    }
}

class T1 {
    public int square (int n) {
        return (int) java.lang.Math.pow(n,2);
    }
    public static void main(String[] arg) {
        T2 x1 = new T2();
        T1 x2 = new T1();
        double m =x1.square(3);
        x1 = (T2) x2;
        System.out.println(m);
    }
}

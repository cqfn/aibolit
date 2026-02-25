// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class OverloadedDiffComp {

    private OverloadedDiffComp a;
    private float b;

    public void method(double b, int a) {
        this.a++;
    }

    public void method(Double b, int a) {
        this.b++;
    }

    public void method3() {
        int a = 1;
        Double e = 0.0001;
        double g = e.doubleValue() + 0.0002;
        method(b, a);
        method(g, a);
    }
}

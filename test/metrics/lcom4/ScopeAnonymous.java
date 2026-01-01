// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class ScopeAnonymous {

    private int a;
    private int b;
    private int c;

    public abstract class Blabla {
        public abstract int ggggg();
        public int method2() {}
    }

    public int method1() {
        ++b;
        return 0;
    }

    public int method2() {
        ++a;
        ++b;
        return 1;
    }

    public int method3() {
        c++;
        return 0;
    }
}

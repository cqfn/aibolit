// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

class MethodChain {

    private int a;
    private int b;

    public Object chain1() {
        ++a;
        return new Object();
    }

    public Object chain2() {
        ++b;
        ++a;
        return new Object();
    }

    public Object chain3() {
    }
}

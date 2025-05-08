// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class Constrc extends Overloaded {

    private int b;

    Constrc(int a) {
        super(a);
    }

    public int method() {
        this.b++;
        return 1;
    }
}

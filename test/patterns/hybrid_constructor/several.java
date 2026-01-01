// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
    private Integer x, y;

    public Foo() {
        int b = 2;
        this(1);
        int a = 1;
    }

    public Foo(int c) {
        int b = 2;
        this(Integer(c));
        int a = 1;
    }

    public Foo(double x) {
        this(1);
    }

    public Foo(Integer x) {
        this(x * 2);
        this.y = x;
    }
    public int square (int n) {
        return n * n;
    }

}

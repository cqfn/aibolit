// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

import java.util.ArrayList;

class Test {
    public void start() {
        ArrayList<Boolean> list = new ArrayList<>();

        if (true) {
            Integer a = 1, b = 2;
            Integer c = a + b;
            Integer d = 1 + b;
            System.out.println(a + b);
        }
    }
}

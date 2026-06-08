// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.ArrayList;

public class SubClass extends SuperClass {

    class NestedTest extends SuperClass1 {

        public NestedTest() {
            super();
            ArrayList<Boolean> list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            super.method4();
        }
    }

    public SubClass() {
        System.out.println("subclass method1");
        super.method1();
    }

    public SubClass(String smth) {
        System.out.println("subclass method1");
        super.method3(smth);
    }

    public SubClass(Integer smth) {
        System.out.println("subclass method1");
        NestedTest a = new NestedTest();
    }
}

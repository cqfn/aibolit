// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.ArrayList;

class Test extends SuperClass {

    class NestedTest extends SuperClass1 {

        @Override
        public void nested() {
            ArrayList<Boolean> list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            super.method1();
        }
    }

    public void start() {
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
        list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
        NestedTest a = new NestedTest();
        a.nested();
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

import java.util.ArrayList;

class Test extends SuperClass {

    public void start() {
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
        list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
    }

    @Override
    public void foo() {
        new Thread() {

            @Override
            public void run() {
                ArrayList<Boolean> list = new ArrayList<Boolean>();
                for (int i = 0; i < 10; i++)
                    for (int j = 0; j < 10; j++)
                        list.add(Boolean.FALSE);
                super.method1();
            }
        }.start();
    }
}

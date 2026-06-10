// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.ArrayList;

class Test {

    public void start() {
        ArrayList<Boolean> list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
        list = new ArrayList<Boolean>();
        for (int i = 0; i < 10; i++)
            list.add(Boolean.FALSE);
    }

    public void foo() {
        new Thread() {
            public void run() {
                ArrayList<Boolean> list = new ArrayList<Boolean>();
                for (int i = 0; i < 10; i++)
                    for (int j = 0; j < 10; j++)
                        list.add(Boolean.FALSE);
            }
        }.start();
    }
}

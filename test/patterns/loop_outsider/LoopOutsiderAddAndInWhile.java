// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

public class LoopOutsiderAddAndInWhile {
    public void loopOutsiderAddAndInWhile() {
        int x = 0;
         for (int i = 0 ; i< 10; i++){
            x += 1; // here
            x++;
            Integer a = 0;

            a &=1;
            a ^=1;

            a++;
            ++a;

        }
    }
}

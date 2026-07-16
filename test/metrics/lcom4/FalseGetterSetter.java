// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class FalseGetterSetter {

    private int first;

    private int second;

    public void setup() {
        first++;
        second++;
    }

    public int getaway() {
        first++;
        return second;
    }

    public void useFirst() {
        first++;
    }

    public void useSecond() {
        second++;
    }
}

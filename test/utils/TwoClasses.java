// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

package two.classes;

class First {
    private int x = 0;

    public int Increment() {
        x += 1;
        return x;
    }
}

class Second {
    private int x = 0;
    private int y = 0;

    public int Decrement() {
        y -= 1;
        return y;
    }

    public int Increment() {
        x += 1;
        return x;
    }
}

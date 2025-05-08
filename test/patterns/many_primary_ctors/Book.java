// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Book {
    private final int a;

    Book(int x) {
        this.a = x;
    }

    Book() {
        this.a = 0;
    }

    Book() {
        this(0);
    }
}

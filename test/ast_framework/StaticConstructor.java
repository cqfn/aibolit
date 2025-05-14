// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

public class ClassWithStaticConstructor {
    static {
        ClassWithStaticConstructor.print("Hello");
        ClassWithStaticConstructor.print("World");
    }

    static private void print(String message) {
        System.out.println(message);
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total RFC = 4

public class FirstClass {
    public void firstPublicMethod() {               // +1 for public method
        System.out.println("Hello World!");         // +1 for invocation
    }

    public void secondPublicMethod() {              // +1 for public method
        System.out.println("Goodbye World!");       // println was already invoked on line 5
        firstPrivateMethod();                       // +1 for invocation
        firstPrivateMethod();                       // firstPrivateMethod was already invoked on line 10
    }

    private void firstPrivateMethod() {
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total RFC = 4

public class FirstClass {
    public void firstPublicMethod() {           // +1 for public method
        System.out.println("Hello World!");     // +1 for invocation (outer method)
    }

    public void secondPublicMethod() {          // +1 for public method
        println();                              // +1 for invocation (local method)
    }

    private void println() {
    }
}

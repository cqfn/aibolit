// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total RFC = 3

public class FirstClass {
    public void firstPublicMethod() {   // +1 for public method
        firstPrivateMethod();           // +1 for invocation
    }

    public void secondPublicMethod() {  // +1 for public method
    }

    private void firstPrivateMethod() {
        secondPrivateMethod();          // invocation inside private methods do not count
    }

    private void secondPrivateMethod() {
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total RFC = 3

public class FirstClass {
    public void firstPublicMethod() {   // +1 for public method
        secondPublicMethod();           // +1 for invocation
    }

    public void secondPublicMethod() {  // +1 for public method
    }
}

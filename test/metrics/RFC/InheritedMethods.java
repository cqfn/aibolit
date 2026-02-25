// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total RFC = 2

public class BaseClass {                            // class RFC = 1
    public void baseMethod() {                      // +1 for public method
    }
}

public class DerivedClass extends BaseClass {       // class RFC = 1
    public void publicMethod() {                    // +1 for public method
        baseMethod();                               // calling inherited method do not count
    }
}

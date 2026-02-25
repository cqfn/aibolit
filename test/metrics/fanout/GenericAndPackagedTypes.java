// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total FanOut = 2

import SomePackage;
import AnotherPackage.GenericType;

public class FirstClass {
    Map<SomePackage.SomeClass, GenericType<SomePackage.SomeClass>> field;       // +2 for SomeClass and GenericType
}

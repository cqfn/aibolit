// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.Arrays;
import AbstractClass.AbstractClass;

public class SingleClass {
    Object synchronizationField = new Object();

    public void nestedScopeWithCycle() {
        while(true) {
            synchronized(synchronizationField) {            // pattern found this line
                int x = 0;
            }
        }
    }

    public void nestedScopeWithLambda() {
        int[] array = { 5, 4, 3, 2, 1 };
        Arrays.sort(array, (firstItem, secondItem) -> {
            synchronized(synchronizationField) {            // pattern found this line
                return firstItem < secondItem;
            }
        });
    }

    public void nestedScopeWithAnonymousClass() {
        Object o = new AbstractClass() {
            void nestedMethod() {
                synchronized(synchronizationField) {        // pattern found this line
                    int x = 0;
                }
            }
        };
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class SingleClass {
    int synchronizationField = 0;

    public SingleClass() {
        synchronized(synchronizationField) {
            int x = 0;
        }
    }

    public void method() {
        synchronized(synchronizationField) {
            int x = 0;
        }
    }
}

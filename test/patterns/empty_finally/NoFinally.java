// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class NoFinally {
    void test() {
        try {
            int x = 1;
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

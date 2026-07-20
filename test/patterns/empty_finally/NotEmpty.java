// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class NotEmpty {
    void test() {
        try {
            int x = 1;
        } finally {
            System.out.println("finally");
        }
    }
}

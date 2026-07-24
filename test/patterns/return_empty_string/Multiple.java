// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class Multiple {
    public String first() {
        return "";
    }

    public String second() {
        String x = "not empty";
        return x;
    }

    public String third() {
        return "";
    }
    
    // Added to cover ternary operator with empty strings in both branches
    public String ternaryBothEmpty(boolean condition) {
        return condition ? "" : "";
    }
}

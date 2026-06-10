// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class LocalMethodCalls {

    private final String variable;

    LocalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }

    public int quantity() {
        return this.value().length();
    }

    public String lower() {
        return this.value().toLowerCase();
    }

    public String upper() {
        return value().toUpperCase();
    }

    public boolean compare(final String another) {
        return this.lower().compareTo(another.toLowerCase());
    }

}

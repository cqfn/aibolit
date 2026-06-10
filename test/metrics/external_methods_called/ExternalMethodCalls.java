// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class ExternalMethodCalls {

    private final String variable;

    NoExternalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }

    public int quantity() {
        return this.variable.length();
    }

    public String lower() {
        return this.variable.toLowerCase();
    }
}

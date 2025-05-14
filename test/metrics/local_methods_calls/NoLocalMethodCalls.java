// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

public class NoLocalMethodCalls {

    private final String variable;

    NoLocalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }
}

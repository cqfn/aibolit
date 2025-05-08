// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
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

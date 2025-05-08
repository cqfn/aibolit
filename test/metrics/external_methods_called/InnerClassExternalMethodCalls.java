// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class InnerClassExternalMethodCalls {

    private final String variable;

    InnerClassExternalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }

    class Upper {

        final String text;

        Upper (final String text) {
            this.text = text;
        }

        public String value() {
            return this.value.toUpperCase();
        }
    }

}

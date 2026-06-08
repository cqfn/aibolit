// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class InnerClassLocalMethodCalls {

    private final String variable;

    InnerClassLocalMethodCalls(final String value) {
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

        public String origin() {
            return this.text;
        }

        public String value() {
            return this.origin().toUpperCase();
        }
    }

    class Lower {

        final String text;

        Lower (final String text) {
            this.text = text;
        }

        public String origin() {
            return this.text;
        }

        public String value() {
            return origin().toLowerCase();
        }
    }
}

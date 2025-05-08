// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class InnerClassProtectedMethod {
    protected void protectedMethodOuter() {

    }

    void notProtectedMethodOuter() {

    }

    class Inner {
        protected void protectedMethodInner() {

        }
    }

}

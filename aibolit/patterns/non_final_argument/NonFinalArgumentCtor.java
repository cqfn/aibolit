// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

package patterns.non_final_argument;

public class NonFinalArgumentCtor {

    private final argument;

    public NonFinalArgumentCtor(int argument) {
        this.argument = argument;
    }

    public int method(final int argument) {
        return argument;
    }
}

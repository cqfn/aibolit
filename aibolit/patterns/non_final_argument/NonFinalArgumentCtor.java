// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
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

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

package patterns.non_final_argument;

public class NonFinalArgumentMethod {

    private final argument;

    public NonFinalArgumentMethod(final int argument) {
        this.argument = argument;
    }

    public int method(int argument) {
        return argument;
    }
}

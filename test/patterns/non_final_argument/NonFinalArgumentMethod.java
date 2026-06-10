// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package patterns.non_final_argument;

public class NonFinalArgumentMethod {

    private final int argument;

    public NonFinalArgumentMethod(final int argument) {
        this.argument = argument;
    }

    public int method(int argument) {
        return argument;
    }
}

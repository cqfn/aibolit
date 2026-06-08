// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import Something;

class Example {
    int field = 0;

    int method(int method_parameter) {
        for(int block_variable; block_variable < method_parameter; ++block_variable) {
            field += block_variable * Something.outer_field;
        }

        return this.field;
    }
}

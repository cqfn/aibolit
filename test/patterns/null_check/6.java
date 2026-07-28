// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

import java.util.function.Predicate;

class Lambda {
    void x() {
        Predicate<String> check = s -> s == null;
    }
}

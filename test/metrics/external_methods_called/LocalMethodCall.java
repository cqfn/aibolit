// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class LocalMethodCall {

    public String value() {
        return "value";
    }

    public String call() {
        return this.value();
    }
}

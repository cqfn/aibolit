// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class PrivateStaticMethod {
    private static String both(int id) {
    }
    private String onlyPrivate(int id) {
    }
    static String onlyStatic(int id) {
    }
    String none(int id) {
    }
}

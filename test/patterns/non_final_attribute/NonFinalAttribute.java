// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class NonFinalAttribute {
    private String nonFinalPrivate = "Non-final";
    private final String finalPrivate = "Non-final";
    public String nonFinalPublic = "Non-final";
    public final String finalPublic = "Non-final";
    protected String nonFinalProtected = "Non-final";
    protected final String finalProtected = "Non-final";
    String nonFinalDefault1 = "Non-final";
    final String finalDefault1 = "Non-final";
}

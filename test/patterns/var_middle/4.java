// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

package org.takes.http;

public final class BkBasic implements Back {
    private static Response failure(final Throwable err, final int code)
        throws IOException {



        final ByteArrayOutputStream baos = new ByteArrayOutputStream();
        try (PrintStream stream = new Utf8PrintStream(baos, false)) {
            err.printStackTrace(stream);
        }
        return new RsWithStatus(
            new RsText(new ByteArrayInputStream(baos.toByteArray())),
            code
        );
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package org.takes.http;

public final class BkBasic implements Back {
    private static Response failure(final Throwable err, final int code)
        throws IOException {
        super.zhop();
        final ByteArrayOutputStream baos = new ByteArrayOutputStream();

        String a = "sdfsdf";

        try (PrintStream stream = new Utf8PrintStream(baos, false)) {
            err.printStackTrace(stream);
        }
        String b = "asdfasdf" + a;
        return new RsWithStatus(
            new RsText(new ByteArrayInputStream(baos.toByteArray())),
            code,
            b
        );
    }

    private static Response success(final Throwable err, final int code) {
        final ByteArrayOutputStream baos = new ByteArrayOutputStream();
    }
}

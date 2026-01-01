// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public final class RqMtFake implements RqMultipart {
    private static final String BOUNDARY = "AaB02x";
    private static final String CRLF = "\r\n";

    @SuppressWarnings(
        {
            "PMD.InsufficientStringBufferDeclaration",
            "PMD.AvoidInstantiatingObjectsInLoops"
        })
    private static StringBuilder fakeBody(final Request... parts)
        throws IOException {
        final StringBuilder builder = new StringBuilder();
        for (final Request part : parts) {
            builder.append(String.format("--%s", RqMtFake.BOUNDARY))
                .append(RqMtFake.CRLF)
                .append("Content-Disposition: ")
                .append(
                    new RqHeaders.Smart(
                        new RqHeaders.Base(part)
                    ).single("Content-Disposition")
                ).append(RqMtFake.CRLF);
            final String body = new RqPrint(part).printBody();
            if (!(RqMtFake.CRLF.equals(body) || body.isEmpty())) {
                builder.append(RqMtFake.CRLF)
                    .append(body)
                    .append(RqMtFake.CRLF);
            }
        }
        builder.append("Content-Transfer-Encoding: utf-8")
            .append(RqMtFake.CRLF)
            .append(String.format("--%s--", RqMtFake.BOUNDARY));
        return builder;
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.http;

import com.artipie.Settings;
import com.artipie.asto.Key;
import com.artipie.http.rq.RequestLineFrom;
import com.artipie.http.rs.RsStatus;
import com.artipie.http.rs.RsWithBody;
import com.artipie.http.rs.RsWithStatus;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.reactivestreams.Publisher;

/**
 * Slice which finds repository by path.
 * @since 0.9
 */
final class SliceByPath implements Slice {

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * Repositories.
     */
    private final Repositories repositories;

    /**
     * New slice from settings.
     * @param settings Artipie settings
     */
    SliceByPath(final Settings settings) {
        this(settings, new ArtipieRepositories(settings));
    }

    /**
     * New slice from settings and repositories.
     * @param settings Artipie settings
     * @param repositories Repositories provider
     */
    SliceByPath(final Settings settings, final Repositories repositories) {
        this.settings = settings;
        this.repositories = repositories;
    }

    // @checkstyle ReturnCountCheck (20 lines)
    @Override
    @SuppressWarnings("PMD.OnlyOneReturn")
    public Response response(final String line, final Iterable<Map.Entry<String, String>> headers,
        final Publisher<ByteBuffer> body) {
        final Key key;
        try {
            final String[] split = new RequestLineFrom(line).uri().getPath()
                .replaceAll("^/+", "").split("/");
            if (this.settings.layout().equals("org")) {
                if (split.length < 2) {
                    throw new IllegalStateException("Expected at least 2 path segments");
                }
                key = new Key.From(split[0], split[1]);
            } else {
                if (split.length < 1) {
                    throw new IllegalStateException("Expected at least 1 path segment");
                }
                key = new Key.From(split[0]);
            }
            return this.repositories.slice(key).response(line, headers, body);
        } catch (final IOException err) {
            return new RsWithBody(
                new RsWithStatus(RsStatus.INTERNAL_ERROR),
                "Failed to parse repository config",
                StandardCharsets.UTF_8
            );
        }
    }
}

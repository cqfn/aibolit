/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import com.artipie.http.Headers;
import com.artipie.http.Response;
import com.artipie.http.Slice;
import com.artipie.http.async.AsyncResponse;
import com.artipie.http.rs.RsWithBody;
import com.artipie.http.rs.RsWithHeaders;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.reactivestreams.Publisher;

/**
 * Slice to render HTML pages.
 * @since 0.10
 */
final class PageSlice implements Slice {

    /**
     * HTML page.
     */
    private final Page page;

    /**
     * New slice for page.
     * @param page Page
     */
    PageSlice(final Page page) {
        this.page = page;
    }

    @Override
    public Response response(final String line, final Iterable<Map.Entry<String, String>> headers,
        final Publisher<ByteBuffer> body) {
        return new RsWithHeaders(
            new AsyncResponse(
                this.page.render(line, headers)
                    .map(html -> new RsWithBody(html, StandardCharsets.UTF_8))
            ),
            new Headers.From("Content-Type", "text/html")
        );
    }
}

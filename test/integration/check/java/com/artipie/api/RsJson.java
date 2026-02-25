/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.api;

import com.artipie.http.Connection;
import com.artipie.http.Headers;
import com.artipie.http.Response;
import com.artipie.http.headers.Header;
import com.artipie.http.rs.RsStatus;
import io.reactivex.Flowable;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletionStage;
import java.util.function.Supplier;
import javax.json.JsonStructure;

/**
 * Response with Yaml document.
 * @since 0.6
 */
public final class RsJson implements Response {

    /**
     * Json supplier.
     */
    private final Supplier<? extends JsonStructure> json;

    /**
     * Charset encoding.
     */
    private final Charset encoding;

    /**
     * Response from Json structure.
     * @param json Json structure
     */
    public RsJson(final JsonStructure json) {
        this(() -> json);
    }

    /**
     * Response from Json supplier.
     * @param json Json supplier
     */
    public RsJson(final Supplier<? extends JsonStructure> json) {
        this(json, StandardCharsets.UTF_8);
    }

    /**
     * Response from Json supplier with charset encoding.
     * @param json Json supplier
     * @param encoding Charset encoding
     */
    public RsJson(final Supplier<? extends JsonStructure> json, final Charset encoding) {
        this.json = json;
        this.encoding = encoding;
    }

    @Override
    public CompletionStage<Void> send(final Connection connection) {
        final byte[] bytes = this.json.get().toString().getBytes(this.encoding);
        return connection.accept(
            RsStatus.OK,
            new Headers.From(
                new Header(
                    "content-type",
                    String.format("application/json; charset=%s", this.encoding.displayName())
                ),
                new Header("content-length", Integer.toString(bytes.length))
            ),
            Flowable.just(ByteBuffer.wrap(bytes))
        );
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.api;

import com.amihaiemil.eoyaml.Yaml;
import com.amihaiemil.eoyaml.YamlMapping;
import com.artipie.asto.Concatenation;
import com.artipie.asto.Remaining;
import io.reactivex.Single;
import io.reactivex.functions.Function;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import org.reactivestreams.Publisher;

/**
 * Rx publisher transformer to single.
 * @param <T> Single type
 * @since 0.8
 */
public final class ContentAs<T>
    implements Function<Single<? extends Publisher<ByteBuffer>>, Single<? extends T>> {

    /**
     * Content as string.
     */
    public static final ContentAs<String> STRING = new ContentAs<>(
        bytes -> new String(bytes, StandardCharsets.UTF_8)
    );

    /**
     * Content as YAML mapping.
     */
    public static final ContentAs<YamlMapping> YAML = new ContentAs<>(
        bytes -> Yaml.createYamlInput(new String(bytes, StandardCharsets.UTF_8))
            .readYamlMapping()
    );

    /**
     * Transform function.
     */
    private final Function<byte[], T> transform;

    /**
     * Ctor.
     * @param transform Transform function
     */
    private ContentAs(final Function<byte[], T> transform) {
        this.transform = transform;
    }

    @Override
    public Single<? extends T> apply(
        final Single<? extends Publisher<ByteBuffer>> content
    ) {
        return content.flatMap(pub -> new Concatenation(pub).single())
            .map(Remaining::new)
            .map(Remaining::bytes)
            .map(this.transform);
    }
}

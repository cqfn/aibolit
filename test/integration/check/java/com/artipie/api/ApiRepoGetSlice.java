/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.api;

import com.amihaiemil.eoyaml.Scalar;
import com.amihaiemil.eoyaml.Yaml;
import com.amihaiemil.eoyaml.YamlMapping;
import com.amihaiemil.eoyaml.YamlMappingBuilder;
import com.artipie.Settings;
import com.artipie.asto.Concatenation;
import com.artipie.asto.Key;
import com.artipie.asto.Remaining;
import com.artipie.asto.rx.RxStorageWrapper;
import com.artipie.http.Response;
import com.artipie.http.Slice;
import com.artipie.http.async.AsyncResponse;
import com.artipie.http.rq.RequestLineFrom;
import com.artipie.http.rs.RsStatus;
import com.artipie.http.rs.RsWithStatus;
import hu.akarnokd.rxjava2.interop.SingleInterop;
import io.reactivex.Single;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.reactivestreams.Publisher;

/**
 * Repo {@code GET} API.
 * @since 0.6
 */
final class ApiRepoGetSlice implements Slice {

    /**
     * URI path pattern.
     */
    private static final Pattern PTN = Pattern.compile("/api/repos/(?<key>[^/.]+/[^/.]+)");

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * New repo API.
     * @param settings Artipie settings
     */
    ApiRepoGetSlice(final Settings settings) {
        this.settings = settings;
    }

    @Override
    @SuppressWarnings("PMD.AvoidDuplicateLiterals")
    public Response response(final String line, final Iterable<Map.Entry<String, String>> headers,
        final Publisher<ByteBuffer> body) {
        final Matcher matcher = PTN.matcher(new RequestLineFrom(line).uri().getPath());
        if (!matcher.matches()) {
            throw new IllegalStateException("Should match");
        }
        final String name = matcher.group("key");
        final Key.From key = new Key.From(String.format("%s.yaml", name));
        // @checkstyle LineLengthCheck (50 lines)
        return new AsyncResponse(
            Single.fromCallable(this.settings::storage).map(RxStorageWrapper::new).flatMap(
                storage -> storage.exists(key).filter(exists -> exists)
                    .flatMapSingleElement(
                        ignore -> storage.value(key)
                            .flatMap(pub -> new Concatenation(pub).single())
                            .map(
                                data -> Yaml.createYamlInput(
                                    new String(new Remaining(data).bytes(), StandardCharsets.UTF_8)
                                ).readYamlMapping()
                            ).map(
                                config -> {
                                    final YamlMapping repo = config.yamlMapping("repo");
                                    YamlMappingBuilder builder = Yaml.createYamlMappingBuilder();
                                    builder = builder.add("type", repo.value("type"));
                                    if (repo.value("storage") != null
                                        && Scalar.class.isAssignableFrom(repo.value("storage").getClass())) {
                                        builder = builder.add("storage", repo.value("storage"));
                                    }
                                    builder = builder.add("permissions", repo.value("permissions"));
                                    return Yaml.createYamlMappingBuilder().add("repo", builder.build()).build();
                                }
                            ).<Response>map(RsYaml::new)
                    ).switchIfEmpty(Single.just(new RsWithStatus(RsStatus.NOT_FOUND)))
            ).to(SingleInterop.get())
        );
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.api;

import com.artipie.Settings;
import com.artipie.asto.Key;
import com.artipie.asto.rx.RxStorageWrapper;
import com.artipie.http.Response;
import com.artipie.http.Slice;
import com.artipie.http.async.AsyncResponse;
import com.artipie.http.rq.RequestLineFrom;
import io.reactivex.Single;
import java.nio.ByteBuffer;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.json.Json;
import javax.json.JsonArrayBuilder;
import javax.json.JsonObjectBuilder;
import org.reactivestreams.Publisher;

/**
 * Repo list API.
 * @since 0.6
 */
final class ApiRepoListSlice implements Slice {

    /**
     * URI path pattern.
     */
    private static final Pattern PTN = Pattern.compile("/api/repos/(?<user>[^/.]+)");

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * New repo list API.
     * @param settings Artipie settings
     */
    ApiRepoListSlice(final Settings settings) {
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
        final String user = matcher.group("user");
        return new AsyncResponse(
            Single.fromCallable(this.settings::storage)
                .map(RxStorageWrapper::new)
                .flatMap(str -> str.list(new Key.From(user)))
                .map(
                    repos -> {
                        final JsonObjectBuilder json = Json.createObjectBuilder()
                            .add("user", user);
                        final JsonArrayBuilder arr = Json.createArrayBuilder();
                        for (final Key key : repos) {
                            arr.add(key.string().replace(".yaml", ""));
                        }
                        json.add("repositories", arr);
                        return json;
                    }
                ).map(builder -> new RsJson(builder::build))
        );
    }
}

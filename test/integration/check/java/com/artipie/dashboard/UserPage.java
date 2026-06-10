/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import com.artipie.Settings;
import com.artipie.asto.Key;
import com.artipie.asto.rx.RxStorageWrapper;
import com.artipie.http.rq.RequestLineFrom;
import com.github.jknack.handlebars.Handlebars;
import com.github.jknack.handlebars.io.TemplateLoader;
import io.reactivex.Single;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.cactoos.map.MapEntry;
import org.cactoos.map.MapOf;

/**
 * User page.
 * @since 0.10
 */
@SuppressWarnings("PMD.AvoidDuplicateLiterals")
final class UserPage implements Page {

    /**
     * URI path pattern.
     */
    private static final Pattern PTN = Pattern.compile("/(?<user>[^/.]+)/?");

    /**
     * Template engine.
     */
    private final Handlebars handlebars;

    /**
     * Settings.
     */
    private final Settings settings;

    /**
     * New page.
     * @param tpl Template loader
     * @param settings Settings
     */
    UserPage(final TemplateLoader tpl, final Settings settings) {
        this.handlebars = new Handlebars(tpl);
        this.settings = settings;
    }

    @Override
    public Single<String> render(final String line,
        final Iterable<Map.Entry<String, String>> headers) {
        final Matcher matcher = PTN.matcher(new RequestLineFrom(line).uri().getPath());
        if (!matcher.matches()) {
            throw new IllegalStateException("Should match");
        }
        final String user = matcher.group("user");
        return Single.fromCallable(this.settings::storage)
            .map(RxStorageWrapper::new)
            .flatMap(str -> str.list(new Key.From(user)))
            .map(
                repos -> this.handlebars.compile("user").apply(
                    new MapOf<>(
                        new MapEntry<>("title", user),
                        new MapEntry<>("user", user),
                        new MapEntry<>(
                            "repos",
                            repos.stream()
                                .map(key -> key.string().replace(".yaml", ""))
                                .collect(Collectors.toList())
                        )
                    )
                )
            );
    }
}

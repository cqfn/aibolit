/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import com.amihaiemil.eoyaml.Scalar;
import com.amihaiemil.eoyaml.Yaml;
import com.amihaiemil.eoyaml.YamlMapping;
import com.amihaiemil.eoyaml.YamlMappingBuilder;
import com.artipie.Settings;
import com.artipie.api.ContentAs;
import com.artipie.asto.Key;
import com.artipie.asto.rx.RxStorageWrapper;
import com.artipie.http.rq.RequestLineFrom;
import com.github.jknack.handlebars.Handlebars;
import com.github.jknack.handlebars.helper.ConditionalHelpers;
import com.github.jknack.handlebars.io.TemplateLoader;
import io.reactivex.Single;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.http.NameValuePair;
import org.apache.http.client.utils.URLEncodedUtils;
import org.cactoos.map.MapEntry;
import org.cactoos.map.MapOf;

/**
 * Repository page.
 * @since 0.10
 */
@SuppressWarnings("PMD.AvoidDuplicateLiterals")
final class RepoPage implements Page {

    /**
     * URI path pattern.
     */
    private static final Pattern PTN = Pattern.compile("/(?<key>[^/.]+/[^/.]+)/?");

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
     * @param tpl Template engine
     * @param settings Settings
     */
    RepoPage(final TemplateLoader tpl, final Settings settings) {
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
        final String name = matcher.group("key");
        this.handlebars.registerHelper("eq", ConditionalHelpers.eq);
        final String[] parts = name.split("/");
        final Key.From key = new Key.From(String.format("%s.yaml", name));
        // @checkstyle LineLengthCheck (30 lines)
        return Single.fromCallable(this.settings::storage).map(RxStorageWrapper::new).flatMap(
            storage -> storage.exists(key).filter(exists -> exists).flatMapSingleElement(
                ignore -> storage.value(key).to(ContentAs.YAML).map(
                    config -> {
                        final YamlMapping repo = config.yamlMapping("repo");
                        YamlMappingBuilder builder = Yaml.createYamlMappingBuilder();
                        builder = builder.add("type", repo.value("type"));
                        if (repo.value("storage") != null
                            && Scalar.class.isAssignableFrom(repo.value("storage").getClass())) {
                            builder = builder.add("storage", repo.value("storage"));
                        }
                        builder = builder.add("permissions", repo.value("permissions"));
                        if (repo.value("settings") != null) {
                            builder = builder.add("settings", repo.value("settings"));
                        }
                        return Yaml.createYamlMappingBuilder().add("repo", builder.build()).build();
                    }
                ).map(
                    yaml -> this.handlebars.compile("repo").apply(
                        new MapOf<>(
                            new MapEntry<>("title", name),
                            new MapEntry<>("user", parts[0]),
                            new MapEntry<>("name", parts[1]),
                            new MapEntry<>("config", yaml.toString()),
                            new MapEntry<>("found", true),
                            new MapEntry<>("type", yaml.yamlMapping("repo").value("type").asScalar().value())
                        )
                    )
                )
            ).switchIfEmpty(
                Single.fromCallable(
                    () -> this.handlebars.compile("repo").apply(
                        new MapOf<>(
                            new MapEntry<>("title", name),
                            new MapEntry<>("user", parts[0]),
                            new MapEntry<>("name", parts[1]),
                            new MapEntry<>("found", false),
                            new MapEntry<>(
                                "type",
                                URLEncodedUtils.parse(
                                    new RequestLineFrom(line).uri(),
                                    StandardCharsets.UTF_8.displayName()
                                ).stream()
                                    .filter(pair -> "type".equals(pair.getName()))
                                    .findFirst().map(NameValuePair::getValue)
                                    .orElse("maven")
                            )
                        )
                    )
                )
            )
        );
    }
}

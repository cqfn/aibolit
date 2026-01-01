/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie;

import com.amihaiemil.eoyaml.Yaml;
import com.amihaiemil.eoyaml.YamlMapping;
import com.artipie.asto.Remaining;
import com.artipie.asto.Storage;
import com.artipie.auth.AuthFromEnv;
import com.artipie.auth.AuthFromYaml;
import com.artipie.auth.ChainedAuth;
import com.artipie.auth.GithubAuth;
import com.artipie.http.auth.Authentication;
import com.artipie.http.slice.KeyFromPath;
import com.jcabi.log.Logger;
import hu.akarnokd.rxjava2.interop.SingleInterop;
import io.reactivex.Flowable;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionStage;
import org.reactivestreams.Publisher;

/**
 * Settings built from YAML.
 *
 * @since 0.1
 * @checkstyle ReturnCountCheck (500 lines)
 */
public final class YamlSettings implements Settings {

    /**
     * Meta section.
     */
    private static final String KEY_META = "meta";

    /**
     * YAML file content.
     */
    private final String content;

    /**
     * Ctor.
     * @param content YAML file content.
     */
    public YamlSettings(final String content) {
        this.content = content;
    }

    @Override
    public Storage storage() throws IOException {
        return new YamlStorage(
            Yaml.createYamlInput(this.content)
                .readYamlMapping()
                .yamlMapping(YamlSettings.KEY_META)
                .yamlMapping("storage")
        ).storage();
    }

    @Override
    @SuppressWarnings("PMD.OnlyOneReturn")
    public CompletionStage<Authentication> auth() {
        final YamlMapping cred;
        try {
            cred = Yaml.createYamlInput(this.content)
                .readYamlMapping()
                .yamlMapping(YamlSettings.KEY_META)
                .yamlMapping("credentials");
        } catch (final IOException err) {
            return CompletableFuture.failedFuture(err);
        }
        final CompletionStage<Authentication> res;
        final String path = "path";
        if (YamlSettings.hasTypeFile(cred) && cred.string(path) != null) {
            final Storage strg;
            try {
                strg = this.storage();
            } catch (final IOException err) {
                return CompletableFuture.failedFuture(err);
            }
            final KeyFromPath key = new KeyFromPath(cred.string(path));
            res = strg.exists(key).thenCompose(
                exists -> {
                    final CompletionStage<Authentication> auth;
                    if (exists) {
                        auth = strg.value(key).thenCompose(
                            file -> yamlFromPublisher(file).thenApply(AuthFromYaml::new)
                        );
                    } else {
                        auth = CompletableFuture.completedStage(new AuthFromEnv());
                    }
                    return auth;
                }
            ).thenApply(
                auth -> new ChainedAuth(new GithubAuth(), auth)
            );
        } else if (YamlSettings.hasTypeFile(cred)) {
            res = CompletableFuture.failedFuture(
                new RuntimeException(
                    "Invalid credentials configuration: type `file` requires `path`!"
                )
            );
        } else {
            res = CompletableFuture.completedStage(new AuthFromEnv());
        }
        return res;
    }

    @Override
    public String layout() throws IOException {
        return Yaml.createYamlInput(this.content)
            .readYamlMapping()
            .yamlMapping(YamlSettings.KEY_META)
            .string("layout");
    }

    @Override
    public YamlMapping meta() throws IOException {
        return Yaml.createYamlInput(this.content)
            .readYamlMapping()
            .yamlMapping(YamlSettings.KEY_META);
    }

    /**
     * Check that yaml has `type: file` mapping in the credentials setting.
     * @param cred Credentials yaml section
     * @return True if setting is present
     */
    private static boolean hasTypeFile(final YamlMapping cred) {
        return cred != null && "file".equals(cred.string("type"));
    }

    /**
     * Create async yaml config from content publisher.
     * @param pub Flow publisher
     * @return Completion stage of yaml
     */
    private static CompletionStage<YamlMapping> yamlFromPublisher(
        final Publisher<ByteBuffer> pub
    ) {
        return Flowable.fromPublisher(pub)
            .reduce(
                new StringBuilder(),
                (acc, buf) -> acc.append(
                    new String(new Remaining(buf).bytes(), StandardCharsets.UTF_8)
                )
            )
            .doOnSuccess(yaml -> Logger.debug(RepoConfig.class, "parsed yaml config: %s", yaml))
            .map(content -> Yaml.createYamlInput(content.toString()).readYamlMapping())
            .to(SingleInterop.get())
            .toCompletableFuture();
    }
}

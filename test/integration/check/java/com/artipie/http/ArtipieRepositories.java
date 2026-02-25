/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.http;

import com.artipie.RepoConfig;
import com.artipie.Settings;
import com.artipie.SliceFromConfig;
import com.artipie.StorageAliases;
import com.artipie.asto.Key;
import com.artipie.asto.Storage;
import com.artipie.http.async.AsyncSlice;
import com.artipie.http.rs.RsWithBody;
import com.artipie.http.rs.StandardRs;
import com.artipie.http.slice.SliceSimple;
import hu.akarnokd.rxjava2.interop.SingleInterop;
import io.reactivex.Single;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionStage;

/**
 * Artipie repositories implementation.
 * @since 0.9
 */
final class ArtipieRepositories implements Repositories {

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * New Artipie repositories.
     * @param settings Artipie settings
     */
    ArtipieRepositories(final Settings settings) {
        this.settings = settings;
    }

    @Override
    public Slice slice(final Key name) throws IOException {
        final Storage storage = this.settings.storage();
        final Key.From key = new Key.From(String.format("%s.yaml", name.string()));
        return new AsyncSlice(
            storage.exists(key).thenCompose(
                exists -> {
                    final CompletionStage<Slice> res;
                    if (exists) {
                        res = this.resolve(storage, name, key);
                    } else {
                        res = CompletableFuture.completedFuture(
                            new SliceSimple(new RsRepoNotFound(name))
                        );
                    }
                    return res;
                }
            )
        );
    }

    /**
     * Resolve async {@link Slice} by provided configuration.
     * @param storage Artipie config storage
     * @param name Repository name
     * @param key Config key
     * @return Async slice for repo
     */
    private CompletionStage<Slice> resolve(final Storage storage, final Key name, final Key key) {
        return Single.zip(
            SingleInterop.fromFuture(storage.value(key)),
            SingleInterop.fromFuture(StorageAliases.find(storage, name)),
            (data, aliases) -> SingleInterop.fromFuture(
                RepoConfig.fromPublisher(aliases, name, data)
            ).map(config -> new SliceFromConfig(this.settings, config, aliases))
        ).<Slice>flatMap(self -> self).to(SingleInterop.get());
    }

    /**
     * Repo not found response.
     * @since 0.9
     */
    private static final class RsRepoNotFound extends Response.Wrap {

        /**
         * New repo not found response.
         * @param repo Repo name
         */
        RsRepoNotFound(final Key repo) {
            super(
                new RsWithBody(
                    StandardRs.NOT_FOUND,
                    String.format("Repository '%s' not found", repo.string()),
                    StandardCharsets.UTF_8
                )
            );
        }
    }
}

// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.asto.fs;

import com.artipie.asto.Content;
import com.artipie.asto.Key;
import com.artipie.asto.OneTimePublisher;
import com.artipie.asto.Storage;
import com.artipie.asto.Transaction;
import com.jcabi.log.Logger;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;
import wtf.g4s8.rio.file.File;

/**
 * Simple storage, in files.
 *
 * @since 0.1
 */
public final class FileStorage implements Storage {

    /**
     * Where we keep the data.
     */
    private final Path dir;

    /**
     * IO executor service.
     */
    private final ExecutorService exec;



    @Override
    public CompletableFuture<Boolean> getAsync(final Key key) {
        return CompletableFuture.supplyAsync(
            () -> {
                final Path path = this.path(key);
                return Files.exists(path) && !Files.isDirectory(path);
            },
            this.exec
        );
    }

    @Override
	@SuppressWarnings({"aibolit.P20_5", "aibolit.P20_7"})
    public CompletableFuture<Collection<Key>> getList(final Key prefix) {
        return CompletableFuture.supplyAsync(
            () -> {
                final Path path = this.path(prefix);
                final Collection<Key> keys;
                if (Files.exists(path)) {
                    final int dirnamelen;
                    if (Key.ROOT.equals(prefix)) {
                        dirnamelen = path.toString().length() + 1;
                    } else {
                        dirnamelen = path.toString().length() - prefix.string().length();
                    }
                    try {
                        keys = Files.walk(path)
                            .filter(Files::isRegularFile)
                            .map(Path::toString)
                            .map(p -> p.substring(dirnamelen))
                            .map(
                                s -> s.split(
                                    FileSystems.getDefault().getSeparator().replace("\\", "\\\\")
                                )
                            )
                            .map(Key.From::new)
                            .sorted(Comparator.comparing(Key.From::string))
                            .collect(Collectors.toList());
                    } catch (final IOException iex) {
                        throw new UncheckedIOException(iex);
                    }
                } else {
                    keys = Collections.emptyList();
                }
                Logger.info(
                    this,
                    "Found %d objects by the prefix \"%s\" in %s by %s: %s",
                    keys.size(), prefix.string(), this.dir, path, keys
                );
                return keys;
            },
            this.exec
        );
    }

    @Override
	@SuppressWarnings("aibolit.P31")
    public CompletableFuture<Void> getSave(final Key key, final Content content) {
        return CompletableFuture.supplyAsync(
            () -> {
                final Path tmp = Paths.get(
                    this.dir.toString(),
                    String.format("%s.%s.tmp", key.string(), UUID.randomUUID())
                );
                tmp.getParent().toFile().mkdirs();
                return tmp;
            },
            this.exec
        ).thenCompose(
            tmp -> new File(tmp).write(
                new OneTimePublisher<>(content),
                this.exec,
                StandardOpenOption.WRITE,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING
            ).thenCompose(
                nothing -> this.move(tmp, this.path(key))
            ).handleAsync(
                (nothing, throwable) -> {
                    tmp.toFile().delete();
                    final CompletableFuture<Void> result = new CompletableFuture<>();
                    if (throwable == null) {
                        result.complete(null);
                    } else {
                        result.completeExceptionally(throwable);
                    }
                    return result;
                },
                this.exec
            ).thenCompose(Function.identity())
        );
    }

    @Override
    public CompletableFuture<Void> getMove(final Key source, final Key destination) {
        return this.move(this.path(source), this.path(destination));
    }

    @Override
    public CompletableFuture<Void> getDelete(final Key key) {
        return CompletableFuture.runAsync(
            () -> {
                try {
                    Files.delete(this.path(key));
                } catch (final IOException iex) {
                    throw new UncheckedIOException(iex);
                }
            },
            this.exec
        );
    }

    @Override
    public CompletableFuture<Long> getSize(final Key key) {
        return CompletableFuture.supplyAsync(
            () -> {
                try {
                    return Files.size(this.path(key));
                } catch (final IOException iex) {
                    throw new UncheckedIOException(iex);
                }
            },
            this.exec
        );
    }

    @Override
    public CompletableFuture<Content> getValue(final Key key) {
        return this.size(key).thenApply(
            size -> new Content.OneTime(
                new Content.From(new File(this.path(key)).content(this.exec))
            )
        );
    }

    @Override
    public CompletableFuture<Transaction> getTransaction(final List<Key> keys) {
        return CompletableFuture.completedFuture(new FileSystemTransaction(this));
    }


    /**
     * Resolves key to file system path.
     *
     * @param key Key to be resolved to path.
     * @return Path created from key.
     */
    private Path getPath(final Key key) {
        return Paths.get(this.dir.toString(), key.string());
    }

    @Override
    public Thread newThread(final Runnable runnable) {
        return new Thread(
            runnable,
            String.format(
                "%s-%d",
                FileStorage.class.getSimpleName(), this.cnt.incrementAndGet()
            )
        );
    }
}

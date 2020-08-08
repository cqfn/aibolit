// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed. 


/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2020 artipie.com
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
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

    /**
     * Ctor.
     * @param path The path to the dir
     * @param nothing Just for compatibility
     * @deprecated Use {@link FileStorage#FileStorage(Path)} ctor instead.
     */
    @Deprecated
    @SuppressWarnings("PMD.UnusedFormalParameter")
    public FileStorage(final Path path, final Object nothing) {
        this(path);
    }

    /**
     * Ctor.
     * @param path File path
     */
    public FileStorage(final Path path) {
        this(path, ThreadPool.EXEC);
    }

    /**
     * Ctor.
     * @param path The path to the dir
     * @param exec IO Executor service
     */
    public FileStorage(final Path path, final ExecutorService exec) {
        this.dir = path;
        this.exec = exec;
    }


    @Override
    public CompletableFuture<Void> save(final Key key, final Content content) {
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
}

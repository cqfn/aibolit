/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.Objects;
import org.apache.commons.io.IOUtils;

/**
 * Java bundled resource in {@code ./src/main/resources}.
 * @since 0.9
 */
public final class JavaResource {

    /**
     * Resource name.
     */
    private final String name;

    /**
     * Classloader.
     */
    private final ClassLoader clo;

    /**
     * Java resource for current thread context class loader.
     * @param name Resource name
     */
    public JavaResource(final String name) {
        this(name, Thread.currentThread().getContextClassLoader());
    }

    /**
     * Java resource.
     * @param name Resource name
     * @param clo Class loader
     */
    public JavaResource(final String name, final ClassLoader clo) {
        this.name = name;
        this.clo = clo;
    }

    /**
     * Copy resource data to destination.
     * @param dest Destination path
     * @throws IOException On error
     */
    public void copy(final Path dest) throws IOException {
        try (
            InputStream src = new BufferedInputStream(
                Objects.requireNonNull(this.clo.getResourceAsStream(this.name))
            );
            OutputStream out = Files.newOutputStream(
                dest, StandardOpenOption.CREATE_NEW, StandardOpenOption.WRITE
            )
        ) {
            IOUtils.copy(src, out);
        }
    }
}

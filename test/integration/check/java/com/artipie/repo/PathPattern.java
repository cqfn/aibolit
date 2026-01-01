/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.repo;

import com.artipie.Settings;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.Collections;
import java.util.Map;
import java.util.regex.Pattern;
import org.cactoos.map.MapEntry;
import org.cactoos.map.MapOf;

/**
 * Layout pattern.
 * @since 0.8
 */
@SuppressWarnings("PMD.AvoidDuplicateLiterals")
public final class PathPattern {

    /**
     * Patterns.
     */
    private static final Map<String, Pattern> PATTERNS = Collections.unmodifiableMap(
        new MapOf<>(
            new MapEntry<>("flat", Pattern.compile("/(?:[^/.]+)(/.*)")),
            new MapEntry<>("org", Pattern.compile("/(?:[^/.]+)/(?:[^/.]+)(/.*)"))
        )
    );

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * New layout pattern from settings.
     * @param settings Settings
     */
    public PathPattern(final Settings settings) {
        this.settings = settings;
    }

    /**
     * Layout pattern from settings.
     * @return Regex pattern
     */
    public Pattern pattern() {
        String name;
        try {
            name = this.settings.layout();
        } catch (final IOException err) {
            throw new UncheckedIOException("Failed to parse settings", err);
        }
        if (name == null) {
            name = "flat";
        }
        final Pattern pth = PathPattern.PATTERNS.get(name);
        if (pth == null) {
            throw new IllegalStateException(String.format("Unknown layout name: '%s'", name));
        }
        return pth;
    }
}

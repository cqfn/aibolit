/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.auth;

import com.artipie.http.auth.Authentication;
import java.util.Optional;
import java.util.concurrent.ConcurrentMap;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import org.jruby.util.collections.ConcurrentWeakHashMap;

/**
 * Cached authentication decorator.
 * <p>
 * It remembers the result of decorated authentication provider and returns it
 * instead of calling origin authentication.
 * </p>
 * @since 0.10
 */
public final class CachedAuth implements Authentication {

    /**
     * Decorated auth provider.
     */
    private final Authentication origin;

    /**
     * Cache map.
     */
    private final ConcurrentMap<String, Optional<String>> cache;

    /**
     * Decorates origin auth provider with caching.
     * @param origin Origin auth provider
     */
    public CachedAuth(final Authentication origin) {
        this(origin, new ConcurrentWeakHashMap<>());
    }

    /**
     * Primary constructor.
     * @param origin Origin auth provider
     * @param cache Cache map
     */
    @SuppressWarnings("PMD.ConstructorOnlyInitializesOrCallOtherConstructors")
    CachedAuth(final Authentication origin, final ConcurrentMap<String, Optional<String>> cache) {
        this.origin = origin;
        this.cache = cache;
        Executors.newSingleThreadScheduledExecutor()
            // @checkstyle MagicNumberCheck (1 line)
            .schedule(this.cache::clear, 5, TimeUnit.MINUTES);
    }

    @Override
    public Optional<String> user(final String username, final String password) {
        return this.cache.computeIfAbsent(username, key -> this.origin.user(key, password));
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.auth;

import com.artipie.http.auth.Authentication;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

/**
 * Chained authentication provider, composed by multiple
 * authentication providers invoked by user specified order.
 * <p>
 * Example, this code will check authentication using {@code GithubAuth} provider first,
 * and {@code EnvAuth} then, if first provider didn't resolve the user:
 * <pre><code>
 * new ChainedAuth(
 *   new GithubAuth(),
 *   new EnvAuth()
 * )
 * </code></pre>
 * </p>
 * @since 0.10
 */
public final class ChainedAuth implements Authentication {

    /**
     * Auth providers list.
     */
    private final List<Authentication> list;

    /**
     * New chain from providers.
     * @param providers Providers
     */
    public ChainedAuth(final Authentication... providers) {
        this(Arrays.asList(providers));
    }

    /**
     * New chain from providers list.
     * @param providers List of providers
     */
    public ChainedAuth(final List<Authentication> providers) {
        this.list = Collections.unmodifiableList(providers);
    }

    @Override
    public Optional<String> user(final String username, final String password) {
        Optional<String> result = Optional.empty();
        for (final Authentication auth : this.list) {
            final Optional<String> attempt = auth.user(username, password);
            if (attempt.isPresent()) {
                result = attempt;
                break;
            }
        }
        return result;
    }
}

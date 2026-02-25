/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.auth;

import com.artipie.http.auth.Authentication;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Authentication based on environment variables.
 * @since 0.3
 */
public final class AuthFromEnv implements Authentication {

    /**
     * Environment name for user.
     */
    private static final String ENV_NAME = "ARTIPIE_USER_NAME";

    /**
     * Environment name for password.
     */
    private static final String ENV_PASS = "ARTIPIE_USER_PASS";

    /**
     * Environment variables.
     */
    private final Map<String, String> env;

    /**
     * Default ctor with system environment.
     */
    public AuthFromEnv() {
        this(System.getenv());
    }

    /**
     * Primary ctor.
     * @param env Environment
     */
    public AuthFromEnv(final Map<String, String> env) {
        this.env = env;
    }

    @Override
    @SuppressWarnings("PMD.OnlyOneReturn")
    public Optional<String> user(final String username, final String password) {
        final Optional<String> result;
        // @checkstyle LineLengthCheck (5 lines)
        if (Objects.equals(Objects.requireNonNull(username), this.env.get(AuthFromEnv.ENV_NAME))
            && Objects.equals(Objects.requireNonNull(password), this.env.get(AuthFromEnv.ENV_PASS))) {
            result = Optional.of(username);
        } else {
            result = Optional.of("anonymous");
        }
        return result;
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-License-Identifier: MIT
 */
package com.artipie.http;

import com.artipie.asto.Key;
import java.io.IOException;

/**
 * Repositories HTTP endpoints.
 * @since 0.9
 */
public interface Repositories {

    /**
     * Find slice by name.
     * @param prefix Repository name
     * @return Repository slice
     * @throws IOException On error
     */
    Slice slice(Key prefix) throws IOException;
}

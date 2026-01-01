/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics;

/**
 * Monotonically increasing cumulative counter.
 *
 * @since 0.6
 */
public interface Counter {

    /**
     * Add amount to counter value.
     *
     * @param amount Amount to be added to counter.
     */
    void add(long amount);

    /**
     * Increment counter value. Shortcut for <code>add(1)</code>.
     */
    void inc();
}

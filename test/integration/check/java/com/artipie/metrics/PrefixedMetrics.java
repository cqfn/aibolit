/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics;

/**
 * Metrics that adds prefix to names.
 *
 * @since 0.9
 */
public final class PrefixedMetrics implements Metrics {

    /**
     * Origin metrics.
     */
    private final Metrics origin;

    /**
     * Prefix.
     */
    private final String prefix;

    /**
     * Ctor.
     *
     * @param origin Origin metrics.
     * @param prefix Prefix.
     */
    public PrefixedMetrics(final Metrics origin, final String prefix) {
        this.origin = origin;
        this.prefix = prefix;
    }

    @Override
    public Counter counter(final String name) {
        return this.origin.counter(this.prefix + name);
    }

    @Override
    public Gauge gauge(final String name) {
        return this.origin.gauge(this.prefix + name);
    }
}

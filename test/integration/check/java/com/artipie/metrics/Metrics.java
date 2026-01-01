/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics;

/**
 * Registry of metrics by name.
 *
 * @since 0.6
 */
public interface Metrics {

    /**
     * Get counter metric by name.
     *
     * @param name Name of metric.
     * @return Counter metric instance.
     */
    Counter counter(String name);

    /**
     * Get gauge metric by name.
     *
     * @param name Name of metric.
     * @return Gauge metric instance.
     */
    Gauge gauge(String name);
}

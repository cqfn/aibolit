/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics;

/**
 * Single numerical value that can increase and decrease.
 *
 * @since 0.6
 */
public interface Gauge {

    /**
     * Set gauge value.
     *
     * @param value Updated value.
     */
    void set(long value);
}

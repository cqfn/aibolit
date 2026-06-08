/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics.nop;

import com.artipie.metrics.Metrics;

/**
 * {@link Metrics} implementation that do no operations and store no data.
 *
 * @since 0.9
 */
public final class NopMetrics implements Metrics {

    /**
     * Only instance of {@link NopMetrics}.
     */
    public static final NopMetrics INSTANCE = new NopMetrics();

    /**
     * Ctor.
     */
    private NopMetrics() {
    }

    @Override
    public NopCounter counter(final String name) {
        return NopCounter.INSTANCE;
    }

    @Override
    public NopGauge gauge(final String name) {
        return NopGauge.INSTANCE;
    }
}

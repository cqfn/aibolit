/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics.nop;

import com.artipie.metrics.Gauge;

/**
 * {@link Gauge} implementation that do no operations and store no data.
 *
 * @since 0.9
 */
public final class NopGauge implements Gauge {

    /**
     * Only instance of {@link NopGauge}.
     */
    public static final NopGauge INSTANCE = new NopGauge();

    /**
     * Ctor.
     */
    private NopGauge() {
    }

    @Override
    public void set(final long update) {
        // do nothing
    }
}

/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics.nop;

import com.artipie.metrics.Counter;

/**
 * {@link Counter} implementation that do no operations and store no data.
 *
 * @since 0.9
 */
public final class NopCounter implements Counter {

    /**
     * Only instance of {@link NopCounter}.
     */
    public static final NopCounter INSTANCE = new NopCounter();

    /**
     * Ctor.
     */
    private NopCounter() {
    }

    @Override
    public void add(final long amount) {
        // do nothing
    }

    @Override
    public void inc() {
        // do nothing
    }
}

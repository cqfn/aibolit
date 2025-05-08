/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics.memory;

import com.artipie.metrics.Metrics;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

/**
 * {@link Metrics} implementation storing data in memory.
 *
 * @since 0.9
 * @todo #231:30min Support gauges in InMemoryMetrics.
 *  `InMemoryMetrics.gauge()` method implementation should get or create an `InMemoryGauge` by name
 *  and store it. `InMemoryMetrics.gauges()` method should be added
 *  to create snapshot of existing gauges. Implementations are expected to be similar to counters.
 */
public final class InMemoryMetrics implements Metrics {

    /**
     * Counters by name.
     */
    private final ConcurrentMap<String, InMemoryCounter> cnts = new ConcurrentHashMap<>();

    @Override
    public InMemoryCounter counter(final String name) {
        return this.cnts.computeIfAbsent(name, ignored -> new InMemoryCounter());
    }

    @Override
    public InMemoryGauge gauge(final String name) {
        throw new UnsupportedOperationException();
    }

    /**
     * Get counters snapshot.
     *
     * @return Counters snapshot.
     */
    public Map<String, InMemoryCounter> counters() {
        return new HashMap<>(this.cnts);
    }
}

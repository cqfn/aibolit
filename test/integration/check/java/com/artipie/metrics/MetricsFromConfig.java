/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.metrics;

import com.amihaiemil.eoyaml.YamlMapping;
import com.artipie.metrics.memory.InMemoryMetrics;
import java.time.Duration;
import java.util.Optional;

/**
 * Metrics from config.
 * @since 0.9
 */
public final class MetricsFromConfig {

    /**
     * Metrics section from settings.
     */
    private final YamlMapping settings;

    /**
     * Ctor.
     * @param metrics Yaml settings
     */
    public MetricsFromConfig(final YamlMapping metrics) {
        this.settings = metrics;
    }

    /**
     * Returns {@link Metrics} instance according to configuration.
     * @return Instance of {@link Metrics}.
     */
    public InMemoryMetrics metrics() {
        return Optional.ofNullable(this.settings.string("type"))
            .map(
                type -> {
                    if (!"log".equals(type)) {
                        throw new IllegalArgumentException(
                            String.format("Unsupported metrics type: %s", type)
                        );
                    }
                    return new InMemoryMetrics();
                }
            ).orElseThrow(() -> new IllegalArgumentException("Metrics type is not specified"));
    }

    /**
     * Publishing interval, default interval is 5 seconds.
     * @return Interval
     * @checkstyle MagicNumberCheck (500 lines)
     */
    public Duration interval() {
        return Optional.ofNullable(this.settings.string("interval"))
            .map(interval -> Duration.ofSeconds(Integer.parseInt(interval)))
            .orElse(Duration.ofSeconds(5));
    }
}

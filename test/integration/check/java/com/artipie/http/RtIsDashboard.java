/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.http;

import com.artipie.Settings;
import com.artipie.http.rq.RequestLineFrom;
import com.artipie.http.rt.RtRule;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.Map;

/**
 * Dashboard routing rule.
 * <p>
 * Checks if settings has {@code org} layout and URI is for dashboard.
 * </p>
 * @since 0.9
 */
final class RtIsDashboard implements RtRule {

    /**
     * Artipie settings.
     */
    private final Settings settings;

    /**
     * New routing rule.
     * @param settings Settings
     */
    RtIsDashboard(final Settings settings) {
        this.settings = settings;
    }

    @Override
    public boolean apply(final String line, final Iterable<Map.Entry<String, String>> headers) {
        return isOrg(this.settings)
            && isDashboardPath(new RequestLineFrom(line).uri().getPath());
    }

    /**
     * Check if layout is org.
     * @param settings Artipie settings
     * @return True if org
     */
    private static boolean isOrg(final Settings settings) {
        try {
            return settings.layout().equals("org");
        } catch (final IOException err) {
            throw new UncheckedIOException("Failed to read layout settings", err);
        }
    }

    /**
     * Check if request path is for dashboard.
     * @param path Request path
     * @return True if dashboard
     */
    private static boolean isDashboardPath(final String path) {
        return path.replaceAll("^/+", "").split("/").length <= 2;
    }
}

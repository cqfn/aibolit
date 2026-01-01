/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */

package com.artipie.http;

import com.artipie.Settings;
import com.artipie.api.ArtipieApi;
import com.artipie.dashboard.DashboardSlice;
import com.artipie.http.rq.RequestLineFrom;
import com.artipie.http.rs.RsStatus;
import com.artipie.http.rs.RsWithStatus;
import com.artipie.http.rt.RtPath;
import com.artipie.http.rt.RtRule;
import com.artipie.http.rt.RtRulePath;
import com.artipie.http.rt.SliceRoute;
import com.artipie.http.slice.LoggingSlice;
import java.util.Optional;
import java.util.logging.Level;
import java.util.regex.Pattern;

/**
 * Pie of slices.
 * @since 0.1
 * @checkstyle ReturnCountCheck (500 lines)
 * @checkstyle ClassDataAbstractionCouplingCheck (500 lines)
 */
public final class Pie extends Slice.Wrap {

    /**
     * Route path returns {@code NO_CONTENT} status if path is empty.
     */
    private static final RtPath EMPTY_PATH = (line, headers, body) -> {
        final String path = new RequestLineFrom(line).uri().getPath();
        final Optional<Response> res;
        if (path.equals("*") || path.equals("/")
            || path.replaceAll("^/+", "").split("/").length == 0) {
            res = Optional.of(new RsWithStatus(RsStatus.NO_CONTENT));
        } else {
            res = Optional.empty();
        }
        return res;
    };

    /**
     * Artipie entry point.
     * @param settings Artipie settings
     */
    public Pie(final Settings settings) {
        super(
            new SafeSlice(
                new LoggingSlice(
                    Level.INFO,
                    new DockerRoutingSlice(
                        new SliceRoute(
                            Pie.EMPTY_PATH,
                            new RtRulePath(
                                new RtRule.ByPath(Pattern.compile("/api/?.*")),
                                new ArtipieApi(settings)
                            ),
                            new RtRulePath(
                                new RtIsDashboard(settings), new DashboardSlice(settings)
                            ),
                            new RtRulePath(
                                RtRule.FALLBACK, new SliceByPath(settings)
                            )
                        )
                    )
                )
            )
        );
    }
}

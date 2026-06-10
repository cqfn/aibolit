/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import io.reactivex.Single;
import java.util.Map;

/**
 * HTML page.
 * @since 0.10
 */
interface Page {

    /**
     * Render page to HTML string.
     * @param line Request line
     * @param headers Request headers
     * @return HTML string
     */
    Single<String> render(String line, Iterable<Map.Entry<String, String>> headers);
}

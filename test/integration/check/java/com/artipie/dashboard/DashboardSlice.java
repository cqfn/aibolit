/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.dashboard;

import com.amihaiemil.eoyaml.Yaml;
import com.artipie.Settings;
import com.artipie.YamlPermissions;
import com.artipie.api.AuthApi;
import com.artipie.asto.Concatenation;
import com.artipie.asto.Key;
import com.artipie.asto.Remaining;
import com.artipie.asto.rx.RxStorageWrapper;
import com.artipie.http.Slice;
import com.artipie.http.async.AsyncSlice;
import com.artipie.http.auth.Permission;
import com.artipie.http.auth.SliceAuth;
import com.artipie.http.rt.RtRule;
import com.artipie.http.rt.RtRulePath;
import com.artipie.http.rt.SliceRoute;
import com.github.jknack.handlebars.io.ClassPathTemplateLoader;
import com.github.jknack.handlebars.io.TemplateLoader;
import hu.akarnokd.rxjava2.interop.SingleInterop;
import io.reactivex.Single;
import java.nio.charset.StandardCharsets;
import java.util.regex.Pattern;

/**
 * Slice with dashboard.
 * @since 0.10
 * @checkstyle ClassDataAbstractionCouplingCheck (500 lines)
 */
public final class DashboardSlice extends Slice.Wrap {

    /**
     * New dashboard slice.
     * @param settings Settings
     */
    public DashboardSlice(final Settings settings) {
        this(settings, new ClassPathTemplateLoader("/dashboard", ".hbs"));
    }

    /**
     * Primary ctor.
     * @param settings Settings
     * @param tpl Template loader for pages
     */
    private DashboardSlice(final Settings settings, final TemplateLoader tpl) {
        // @checkstyle LineLengthCheck (100 lines)
        super(
            new AsyncSlice(
                Single.zip(
                    Single.fromCallable(settings::auth).flatMap(SingleInterop::fromFuture),
                    Single.fromCallable(settings::storage).map(RxStorageWrapper::new)
                        .flatMap(storage -> storage.value(new Key.From("_permissions.yaml")).flatMap(data -> new Concatenation(data).single()))
                        .map(buf -> new Remaining(buf).bytes())
                        .map(bytes -> Yaml.createYamlInput(new String(bytes, StandardCharsets.UTF_8)).readYamlMapping())
                        .map(YamlPermissions::new),
                    (auth, perm) -> new SliceAuth(
                        new SliceRoute(
                            new RtRulePath(
                                new RtRule.ByPath(Pattern.compile("/(?:[^/.]+)/?")),
                                new PageSlice(new UserPage(tpl, settings))
                            ),
                            new RtRulePath(
                                new RtRule.ByPath(Pattern.compile("/(?:[^/.]+)/(?:[^/.]+)/?")),
                                new PageSlice(new RepoPage(tpl, settings))
                            )
                        ),
                        new Permission.ByName("api", perm),
                        new AuthApi(auth)
                    )
                ).to(SingleInterop.get())
            )
        );
    }
}

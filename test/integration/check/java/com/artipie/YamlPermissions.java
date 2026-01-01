/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie;

import com.amihaiemil.eoyaml.Scalar;
import com.amihaiemil.eoyaml.Yaml;
import com.amihaiemil.eoyaml.YamlMapping;
import com.amihaiemil.eoyaml.YamlSequence;
import com.artipie.http.auth.Permissions;
import java.io.File;
import java.io.IOException;

/**
 * Repository permissions: this implementation is based on
 * on repository yaml configuration file.
 * @since 0.2
 */
public final class YamlPermissions implements Permissions {

    /**
     * Asterisk wildcard.
     */
    private static final String WILDCARD = "*";

    /**
     * YAML storage settings.
     */
    private final YamlMapping yaml;

    /**
     * Ctor.
     * @param conf Config file
     */
    public YamlPermissions(final File conf) {
        this(readYaml(conf));
    }

    /**
     * Ctor.
     * @param yaml Configuration yaml
     */
    public YamlPermissions(final YamlMapping yaml) {
        this.yaml = yaml;
    }

    @Override
    public boolean allowed(final String name, final String action) {
        final YamlMapping all = this.yaml.yamlMapping("permissions");
        return check(all.yamlSequence(name), action)
            || check(all.yamlSequence(YamlPermissions.WILDCARD), action);
    }

    /**
     * Read provided file into Yaml object.
     * @param conf File
     * @return Yaml mapping
     */
    private static YamlMapping readYaml(final File conf) {
        try {
            return Yaml.createYamlInput(conf).readYamlMapping().yamlMapping("repo");
        } catch (final IOException ex) {
            throw new IllegalArgumentException("Invalid configuration file", ex);
        }
    }

    /**
     * Checks if permissions sequence has a given action.
     * @param seq Permissions
     * @param action Action
     * @return True if action is allowed
     */
    private static boolean check(final YamlSequence seq, final String action) {
        return seq != null && seq.values().stream().map(node -> Scalar.class.cast(node).value())
            .anyMatch(item -> item.equals(action) || item.equals(YamlPermissions.WILDCARD));
    }

}

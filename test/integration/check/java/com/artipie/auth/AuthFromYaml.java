/*
 * SPDX-FileCopyrightText: Copyright (c) 2020 artipie.com
 * SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
 * SPDX-License-Identifier: MIT
 */
package com.artipie.auth;

import com.amihaiemil.eoyaml.YamlMapping;
import com.artipie.http.auth.Authentication;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.commons.codec.digest.DigestUtils;

/**
 * Authentication implementation based on yaml file with credentials.
 * @since 0.3
 */
@SuppressWarnings({
    "PMD.AvoidDeeplyNestedIfStmts",
    "PMD.AvoidDuplicateLiterals",
    "PMD.ConfusingTernary"})
public final class AuthFromYaml implements Authentication {

    /**
     * Password format.
     */
    private static final Pattern PSWD_FORMAT = Pattern.compile("(plain:|sha256:)(.+)");

    /**
     * YAML credentials settings.
     */
    private final YamlMapping cred;

    /**
     * Ctor.
     * @param cred Credentials settings
     */
    public AuthFromYaml(final YamlMapping cred) {
        this.cred = cred;
    }

    @Override
    public Optional<String> user(final String user, final String pass) {
        final YamlMapping users = this.cred.yamlMapping("credentials");
        Optional<String> res = Optional.empty();
        //@checkstyle NestedIfDepthCheck (10 lines)
        if (users != null && users.yamlMapping(user) != null) {
            final String stored = users.yamlMapping(user).string("pass");
            if (stored != null) {
                final String type = users.yamlMapping(user).string("type");
                if (type != null) {
                    if (check(stored, type, pass)) {
                        res = Optional.of(user);
                    }
                } else {
                    if (check(stored, pass)) {
                        res = Optional.of(user);
                    }
                }
            }
        }
        return res;
    }

    /**
     * Checks stored password against the given one with type.
     * @param stored Password from settings
     * @param type Type of Password from settings
     * @param given Password to check
     * @return True if passwords are the same
     */
    private static boolean check(final String stored, final String type, final String given) {
        return type.equals("sha256") && DigestUtils.sha256Hex(given)
            .equals(stored) || given.equals(stored);
    }

    /**
     * Checks stored password against the given one.
     * @param stored Password from settings
     * @param given Password to check
     * @return True if passwords are the same
     */
    private static boolean check(final String stored, final String given) {
        boolean res = false;
        final Matcher matcher = AuthFromYaml.PSWD_FORMAT.matcher(stored);
        if (matcher.matches()) {
            final String pswd = matcher.group(2);
            res = stored.startsWith("sha256") && DigestUtils.sha256Hex(given).equals(pswd)
                || given.equals(pswd);
        }
        return res;
    }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
package com.test;

import java.util.HashMap;
import java.util.Map;

public class ConfigManager {
    private Map<String, String> data = new HashMap<>();
    private int counter = 0;
    private String name = "default";

    public void setValue(String key, String value) { data.put(key, value); counter++; }
    public String getValue(String key) { return data.get(key); }
    public int getCounter() { return counter; }
    public void incrementCounter() { counter++; }
    public String getName() { return name; }
    public void setName(String n) { this.name = n; }
    public void reset() { data.clear(); counter = 0; name = "default"; }
    public boolean hasKey(String key) { return data.containsKey(key); }
    public int size() { return data.size(); }
}

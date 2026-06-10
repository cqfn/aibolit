// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.hadoop.conf;

import com.google.common.annotations.VisibleForTesting;
import com.google.common.base.Preconditions;
import com.google.common.collect.Maps;
import org.apache.hadoop.util.Time;
import org.apache.hadoop.conf.ReconfigurationUtil.PropertyChange;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Collection;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;

/**
 * Utility base class for implementing the Reconfigurable interface.
 *
 * Subclasses should override reconfigurePropertyImpl to change individual
 * properties and getReconfigurableProperties to get all properties that
 * can be changed at run time.
 */
public abstract class ReconfigurableBase
  extends Configured implements Reconfigurable {

  private static final Logger LOG =
      LoggerFactory.getLogger(ReconfigurableBase.class);
  // Use for testing purpose.
  private ReconfigurationUtil reconfigurationUtil = new ReconfigurationUtil();

  /** Background thread to reload configuration. */
  private Thread reconfigThread = null;
  private volatile boolean shouldRun = true;
  private Object reconfigLock = new Object();

  /**
   * The timestamp when the <code>reconfigThread</code> starts.
   */
  private long startTime = 0;

  /**
   * The timestamp when the <code>reconfigThread</code> finishes.
   */
  private long endTime = 0;

  /**
   * A map of <changed property, error message>. If error message is present,
   * it contains the messages about the error occurred when applies the particular
   * change. Otherwise, it indicates that the change has been successfully applied.
   */
  private Map<PropertyChange, Optional<String>> status = null;

  /**
   * Construct a ReconfigurableBase.
   */
  public ReconfigurableBase() {
    super(new Configuration());
  }

  /**
   * Construct a ReconfigurableBase with the {@link Configuration}
   * conf.
   */
  public ReconfigurableBase(Configuration conf) {
    super((conf == null) ? new Configuration() : conf);
  }

  @VisibleForTesting
  public void setReconfigurationUtil(ReconfigurationUtil ru) {
    reconfigurationUtil = Preconditions.checkNotNull(ru);
  }

  /**
   * Create a new configuration.
   */
  protected abstract Configuration getNewConf();

  @VisibleForTesting
  public Collection<PropertyChange> getChangedProperties(
      Configuration newConf, Configuration oldConf) {
    return reconfigurationUtil.parseChangedProperties(newConf, oldConf);
  }

  /**
   * A background thread to apply configuration changes.
   */
  private static class ReconfigurationThread extends Thread {
    private ReconfigurableBase parent;

    ReconfigurationThread(ReconfigurableBase base) {
      this.parent = base;
    }

	    public void run() {
      LOG.info("Starting reconfiguration task.");
      final Configuration oldConf = parent.getConf();
      final Configuration newConf = parent.getNewConf();
      final Collection<PropertyChange> changes =
          parent.getChangedProperties(newConf, oldConf);
      Map<PropertyChange, Optional<String>> results = Maps.newHashMap();
      ConfigRedactor oldRedactor = new ConfigRedactor(oldConf);
      ConfigRedactor newRedactor = new ConfigRedactor(newConf);
      for (PropertyChange change : changes) {
        String errorMessage = null;
        String oldValRedacted = oldRedactor.redact(change.prop, change.oldVal);
        String newValRedacted = newRedactor.redact(change.prop, change.newVal);
        if (!parent.isPropertyReconfigurable(change.prop)) {
          LOG.info(String.format(
              "Property %s is not configurable: old value: %s, new value: %s",
              change.prop,
              oldValRedacted,
              newValRedacted));
          continue;
        }
        LOG.info("Change property: " + change.prop + " from \""
            + ((change.oldVal == null) ? "<default>" : oldValRedacted)
            + "\" to \""
            + ((change.newVal == null) ? "<default>" : newValRedacted)
            + "\".");
        try {
          String effectiveValue =
              parent.reconfigurePropertyImpl(change.prop, change.newVal);
          if (change.newVal != null) {
            oldConf.set(change.prop, effectiveValue);
          } else {
            oldConf.unset(change.prop);
          }
        } catch (ReconfigurationException e) {
          Throwable cause = e.getCause();
          errorMessage = cause == null ? e.getMessage() : cause.getMessage();
        }
        results.put(change, Optional.ofNullable(errorMessage));
      }

      synchronized (parent.reconfigLock) {
        parent.endTime = Time.now();
        parent.status = Collections.unmodifiableMap(results);
        parent.reconfigThread = null;
      }
    }
  }
}

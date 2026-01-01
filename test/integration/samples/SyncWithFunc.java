// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
/*
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
package org.apache.hadoop.fs;

import javax.annotation.Nonnull;
import java.io.Closeable;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.ref.WeakReference;
import java.lang.ref.ReferenceQueue;
import java.net.URI;
import java.net.URISyntaxException;
import java.security.PrivilegedExceptionAction;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Optional;
import java.util.ServiceConfigurationError;
import java.util.ServiceLoader;
import java.util.Set;
import java.util.Stack;
import java.util.TreeSet;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.atomic.AtomicLong;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.hadoop.classification.InterfaceAudience;
import org.apache.hadoop.classification.InterfaceStability;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.GlobalStorageStatistics.StorageStatisticsProvider;
import org.apache.hadoop.fs.Options.ChecksumOpt;
import org.apache.hadoop.fs.Options.HandleOpt;
import org.apache.hadoop.fs.Options.Rename;
import org.apache.hadoop.fs.impl.AbstractFSBuilderImpl;
import org.apache.hadoop.fs.impl.FutureDataInputStreamBuilderImpl;
import org.apache.hadoop.fs.impl.OpenFileParameters;
import org.apache.hadoop.fs.permission.AclEntry;
import org.apache.hadoop.fs.permission.AclStatus;
import org.apache.hadoop.fs.permission.FsAction;
import org.apache.hadoop.fs.permission.FsCreateModes;
import org.apache.hadoop.fs.permission.FsPermission;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.io.MultipleIOException;
import org.apache.hadoop.net.NetUtils;
import org.apache.hadoop.security.AccessControlException;
import org.apache.hadoop.security.Credentials;
import org.apache.hadoop.security.SecurityUtil;
import org.apache.hadoop.security.UserGroupInformation;
import org.apache.hadoop.security.token.Token;
import org.apache.hadoop.security.token.DelegationTokenIssuer;
import org.apache.hadoop.util.ClassUtil;
import org.apache.hadoop.util.DataChecksum;
import org.apache.hadoop.util.LambdaUtils;
import org.apache.hadoop.util.Progressable;
import org.apache.hadoop.util.ReflectionUtils;
import org.apache.hadoop.util.ShutdownHookManager;
import org.apache.hadoop.util.StringUtils;
import org.apache.htrace.core.Tracer;
import org.apache.htrace.core.TraceScope;

import com.google.common.base.Preconditions;
import com.google.common.annotations.VisibleForTesting;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import static com.google.common.base.Preconditions.checkArgument;
import static org.apache.hadoop.fs.CommonConfigurationKeysPublic.*;
import static org.apache.hadoop.fs.impl.PathCapabilitiesSupport.validatePathCapabilityArgs;

/****************************************************************
 * An abstract base class for a fairly generic filesystem.  It
 * may be implemented as a distributed filesystem, or as a "local"
 * one that reflects the locally-connected disk.  The local version
 * exists for small Hadoop instances and for testing.
 *
 * <p>
 *
 * All user code that may potentially use the Hadoop Distributed
 * File System should be written to use a FileSystem object or its
 * successor, {@link FileContext}.
 *
 * <p>
 * The local implementation is {@link LocalFileSystem} and distributed
 * implementation is DistributedFileSystem. There are other implementations
 * for object stores and (outside the Apache Hadoop codebase),
 * third party filesystems.
 * <p>
 * Notes
 * <ol>
 * <li>The behaviour of the filesystem is
 * <a href="https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/filesystem/filesystem.html">
 * specified in the Hadoop documentation. </a>
 * However, the normative specification of the behavior of this class is
 * actually HDFS: if HDFS does not behave the way these Javadocs or
 * the specification in the Hadoop documentations define, assume that
 * the documentation is incorrect.
 * </li>
 * <li>The term {@code FileSystem} refers to an instance of this class.</li>
 * <li>The acronym "FS" is used as an abbreviation of FileSystem.</li>
 * <li>The term {@code filesystem} refers to the distributed/local filesystem
 * itself, rather than the class used to interact with it.</li>
 * <li>The term "file" refers to a file in the remote filesystem,
 * rather than instances of {@code java.io.File}.</li>
 * </ol>
 *
 * This is a carefully evolving class.
 * New methods may be marked as Unstable or Evolving for their initial release,
 * as a warning that they are new and may change based on the
 * experience of use in applications.
 *****************************************************************/
@SuppressWarnings("DeprecatedIsStillUsed")
@InterfaceAudience.Public
@InterfaceStability.Stable
public abstract class FileSystem extends Configured
    implements Closeable, DelegationTokenIssuer, PathCapabilities {
  public static final String FS_DEFAULT_NAME_KEY =
                   CommonConfigurationKeys.FS_DEFAULT_NAME_KEY;
  public static final String DEFAULT_FS =
                   CommonConfigurationKeys.FS_DEFAULT_NAME_DEFAULT;

  /**
   * This log is widely used in the org.apache.hadoop.fs code and tests,
   * so must be considered something to only be changed with care.
   */
  @InterfaceAudience.Private
  public static final Log LOG = LogFactory.getLog(FileSystem.class);

  /**
   * The SLF4J logger to use in logging within the FileSystem class itself.
   */
  private static final Logger LOGGER =
      LoggerFactory.getLogger(FileSystem.class);

  /**
   * Priority of the FileSystem shutdown hook: {@value}.
   */
  public static final int SHUTDOWN_HOOK_PRIORITY = 10;

  /**
   * Prefix for trash directory: {@value}.
   */
  public static final String TRASH_PREFIX = ".Trash";
  public static final String USER_HOME_PREFIX = "/user";

  /** FileSystem cache. */
  static final Cache CACHE = new Cache();

  /** The key this instance is stored under in the cache. */
  private Cache.Key key;

  /** Recording statistics per a FileSystem class. */
  private static final Map<Class<? extends FileSystem>, Statistics>
      statisticsTable = new IdentityHashMap<>();

  /**
   * The statistics for this file system.
   */
  protected Statistics statistics;

  /**
   * A cache of files that should be deleted when the FileSystem is closed
   * or the JVM is exited.
   */
  private final Set<Path> deleteOnExit = new TreeSet<>();

  /**
   * Should symbolic links be resolved by {@link FileSystemLinkResolver}.
   * Set to the value of
   * {@link CommonConfigurationKeysPublic#FS_CLIENT_RESOLVE_REMOTE_SYMLINKS_KEY}
   */
  boolean resolveSymlinks;

  /**
   * This method adds a FileSystem instance to the cache so that it can
   * be retrieved later. It is only for testing.
   * @param uri the uri to store it under
   * @param conf the configuration to store it under
   * @param fs the FileSystem to store
   * @throws IOException if the current user cannot be determined.
   */
  @VisibleForTesting
  static void addFileSystemForTesting(URI uri, Configuration conf,
      FileSystem fs) throws IOException {
    CACHE.map.put(new Cache.Key(uri, conf), fs);
  }

  @VisibleForTesting
  static void removeFileSystemForTesting(URI uri, Configuration conf,
      FileSystem fs) throws IOException {
    CACHE.map.remove(new Cache.Key(uri, conf), fs);
  }

  @VisibleForTesting
  static int cacheSize() {
    return CACHE.map.size();
  }


  public boolean deleteOnExit(Path f) throws IOException {
    if (!exists(f)) {
      return false;
    }
    synchronized (deleteOnExit) {
      deleteOnExit.add(f);
    }
    return true;
  }
}

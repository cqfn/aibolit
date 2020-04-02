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
package org.apache.hadoop.hdfs.server.datanode.fsdataset;

import static org.apache.hadoop.hdfs.DFSConfigKeys.DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_THRESHOLD_DEFAULT;
import static org.apache.hadoop.hdfs.DFSConfigKeys.DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_THRESHOLD_KEY;
import static org.apache.hadoop.hdfs.DFSConfigKeys.DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_PREFERENCE_FRACTION_DEFAULT;
import static org.apache.hadoop.hdfs.DFSConfigKeys.DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_PREFERENCE_FRACTION_KEY;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.hadoop.conf.Configurable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.StorageType;
import org.apache.hadoop.util.DiskChecker.DiskOutOfSpaceException;

/**
 * A DN volume choosing policy which takes into account the amount of free
 * space on each of the available volumes when considering where to assign a
 * new replica allocation. By default this policy prefers assigning replicas to
 * those volumes with more available free space, so as to over time balance the
 * available space of all the volumes within a DN.
 * Use fine-grained locks to enable choosing volumes of different storage
 * types concurrently.
 */
public class AvailableSpaceVolumeChoosingPolicy<V extends FsVolumeSpi>
    implements VolumeChoosingPolicy<V>, Configurable {
  
  private static final Logger LOG =
      LoggerFactory.getLogger(AvailableSpaceVolumeChoosingPolicy.class);

  private Object[] syncLocks;
  
  private final Random random;
  
  private long balancedSpaceThreshold = DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_THRESHOLD_DEFAULT;
  private float balancedPreferencePercent = DFS_DATANODE_AVAILABLE_SPACE_VOLUME_CHOOSING_POLICY_BALANCED_SPACE_PREFERENCE_FRACTION_DEFAULT;

  AvailableSpaceVolumeChoosingPolicy(Random random) {
    this.random = random;
    initLocks();
  }

  public AvailableSpaceVolumeChoosingPolicy() {
    this(new Random());
    initLocks();
  }

  private void initLocks() {
    int numStorageTypes = StorageType.values().length;
    syncLocks = new Object[numStorageTypes];
    for (int i = 0; i < numStorageTypes; i++) {
      syncLocks[i] = new Object();
    }
  }

  @Override
  public V chooseVolume(List<V> volumes, long replicaSize, String storageId)
      throws IOException {
    if (volumes.size() < 1) {
      throw new DiskOutOfSpaceException("No more available volumes");
    }
    // As all the items in volumes are with the same storage type,
    // so only need to get the storage type index of the first item in volumes
    StorageType storageType = volumes.get(0).getStorageType();
    int index = storageType != null ?
            storageType.ordinal() : StorageType.DEFAULT.ordinal();

    synchronized (syncLocks[index]) {
      return doChooseVolume(volumes, replicaSize, storageId);
    }
  }

}

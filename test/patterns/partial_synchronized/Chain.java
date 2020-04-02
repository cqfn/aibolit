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
package org.apache.hadoop.hdfs.server.namenode;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertNotNull;

import java.lang.management.ManagementFactory;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import javax.management.MBeanAttributeInfo;
import javax.management.MBeanInfo;
import javax.management.MBeanServer;
import javax.management.ObjectName;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hdfs.MiniDFSCluster;
import org.apache.hadoop.metrics2.impl.ConfigBuilder;
import org.apache.hadoop.metrics2.impl.TestMetricsConfig;
import org.junit.Test;
import org.eclipse.jetty.util.ajax.JSON;

/**
 * Class for testing {@link NameNodeMXBean} implementation
 */
public class TestFSNamesystemMBean {

  /**
   * MBeanClient tries to access FSNamesystem/FSNamesystemState/NameNodeInfo
   * JMX properties. If it can access all the properties, the test is
   * considered successful.
   */
  private static class MBeanClient extends Thread {
    private boolean succeeded = false;
    @Override
    public void run() {
      try {
        MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

        // Metrics that belong to "FSNamesystem", these are metrics that
        // come from hadoop metrics framework for the class FSNamesystem.
        ObjectName mxbeanNamefsn = new ObjectName(
            "Hadoop:service=NameNode,name=FSNamesystem");

        // Metrics that belong to "FSNamesystemState".
        // These are metrics that FSNamesystem registers directly with MBeanServer.
        ObjectName mxbeanNameFsns = new ObjectName(
            "Hadoop:service=NameNode,name=FSNamesystemState");

        // Metrics that belong to "NameNodeInfo".
        // These are metrics that FSNamesystem registers directly with MBeanServer.
        ObjectName mxbeanNameNni = new ObjectName(
            "Hadoop:service=NameNode,name=NameNodeInfo");

        final Set<ObjectName> mbeans = new HashSet<ObjectName>();
        mbeans.add(mxbeanNamefsn);
        mbeans.add(mxbeanNameFsns);
        mbeans.add(mxbeanNameNni);

        for(ObjectName mbean : mbeans) {
          MBeanInfo attributes = mbs.getMBeanInfo(mbean);
          for (MBeanAttributeInfo attributeInfo : attributes.getAttributes()) {
            mbs.getAttribute(mbean, attributeInfo.getName());
          }
        }

        succeeded = true;
      } catch (Exception e) {
      }
    }
  }

  @Test
  public void test() throws Exception {
    Configuration conf = new Configuration();
    MiniDFSCluster cluster = null;

    try {
      cluster = new MiniDFSCluster.Builder(conf).build();
      cluster.waitActive();

      FSNamesystem fsn = cluster.getNameNode().namesystem;

      MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
      ObjectName mxbeanName = new ObjectName(
          "Hadoop:service=NameNode,name=FSNamesystemState");

      String snapshotStats = (String) (mbs.getAttribute(mxbeanName,
          "SnapshotStats"));

      @SuppressWarnings("unchecked")
      Map<String, Object> stat = (Map<String, Object>) JSON
          .parse(snapshotStats);

      assertTrue(stat.containsKey("SnapshottableDirectories")
          && (Long) stat.get("SnapshottableDirectories") == fsn
              .getNumSnapshottableDirs());
      assertTrue(stat.containsKey("Snapshots")
          && (Long) stat.get("Snapshots") == fsn.getNumSnapshots());

      Object pendingDeletionBlocks = mbs.getAttribute(mxbeanName,
        "PendingDeletionBlocks");
      assertNotNull(pendingDeletionBlocks);
      assertTrue(pendingDeletionBlocks instanceof Long);

      Object encryptionZones = mbs.getAttribute(mxbeanName,
          "NumEncryptionZones");
      assertNotNull(encryptionZones);
      assertTrue(encryptionZones instanceof Integer);
    } finally {
      if (cluster != null) {
        cluster.shutdown();
      }
    }
  }

  // The test makes sure JMX request can be processed even if namesystem's
  // writeLock is owned by another thread.
  @Test
  public void testWithFSNamesystemWriteLock() throws Exception {
    Configuration conf = new Configuration();
    MiniDFSCluster cluster = null;
    FSNamesystem fsn = null;

    int jmxCachePeriod = 1;
    new ConfigBuilder().add("namenode.period", jmxCachePeriod)
        .save(TestMetricsConfig.getTestFilename("hadoop-metrics2-namenode"));
    try {
      cluster = new MiniDFSCluster.Builder(conf).build();
      cluster.waitActive();

      fsn = cluster.getNameNode().namesystem;
      fsn.writeLock();
      Thread.sleep(jmxCachePeriod * 1000);

      MBeanClient client = new MBeanClient();
      client.start();
      client.join(20000);
      assertTrue("JMX calls are blocked when FSNamesystem's writerlock" +
          "is owned by another thread", client.succeeded);
      client.interrupt();
    } finally {
      if (fsn != null && fsn.hasWriteLock()) {
        fsn.writeUnlock();
      }
      if (cluster != null) {
        cluster.shutdown();
      }
    }
  }

  // The test makes sure JMX request can be processed even if FSEditLog
  // is synchronized.
  @Test
  public void testWithFSEditLogLock() throws Exception {
    Configuration conf = new Configuration();
    int jmxCachePeriod = 1;
    new ConfigBuilder().add("namenode.period", jmxCachePeriod)
        .save(TestMetricsConfig.getTestFilename("hadoop-metrics2-namenode"));
    MiniDFSCluster cluster = null;
    try {
      cluster = new MiniDFSCluster.Builder(conf).build();
      cluster.waitActive();
      synchronized (cluster.getNameNode().getFSImage().getEditLog()) {
        Thread.sleep(jmxCachePeriod * 1000);
        MBeanClient client = new MBeanClient();
        client.start();
        client.join(20000);
        assertTrue("JMX calls are blocked when FSEditLog" +
            " is synchronized by another thread", client.succeeded);
        client.interrupt();
      }
    } finally {
      if (cluster != null) {
        cluster.shutdown();
      }
    }
  }

  @Test(timeout = 120000)
  public void testFsEditLogMetrics() throws Exception {
    final Configuration conf = new Configuration();
    MiniDFSCluster cluster = null;
    try {
      cluster = new MiniDFSCluster.Builder(conf).numDataNodes(0).build();
      cluster.waitActive();
      MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();
      ObjectName mxbeanNameFs =
          new ObjectName("Hadoop:service=NameNode,name=FSNamesystemState");

      FileSystem fs = cluster.getFileSystem();
      final int NUM_OPS = 10;
      for (int i = 0; i < NUM_OPS; i++) {
        final Path path = new Path(String.format("/user%d", i));
        fs.mkdirs(path);
      }

      long syncCount = (long) mbs.getAttribute(mxbeanNameFs, "TotalSyncCount");
      String syncTimes =
          (String) mbs.getAttribute(mxbeanNameFs, "TotalSyncTimes");
      assertTrue(syncCount > 0);
      assertNotNull(syncTimes);
    } finally {
      if (cluster != null) {
        cluster.shutdown();
      }
    }
  }
}

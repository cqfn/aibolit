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
 * <p>
 * http://www.apache.org/licenses/LICENSE-2.0
 * <p>
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.hadoop.fs.cosn;

import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.concurrent.ThreadLocalRandom;

import com.qcloud.cos.COSClient;
import com.qcloud.cos.ClientConfig;
import com.qcloud.cos.auth.BasicCOSCredentials;
import com.qcloud.cos.auth.COSCredentials;
import com.qcloud.cos.exception.CosClientException;
import com.qcloud.cos.exception.CosServiceException;
import com.qcloud.cos.http.HttpProtocol;
import com.qcloud.cos.model.AbortMultipartUploadRequest;
import com.qcloud.cos.model.COSObject;
import com.qcloud.cos.model.COSObjectSummary;
import com.qcloud.cos.model.CompleteMultipartUploadRequest;
import com.qcloud.cos.model.CompleteMultipartUploadResult;
import com.qcloud.cos.model.CopyObjectRequest;
import com.qcloud.cos.model.DeleteObjectRequest;
import com.qcloud.cos.model.GetObjectMetadataRequest;
import com.qcloud.cos.model.GetObjectRequest;
import com.qcloud.cos.model.InitiateMultipartUploadRequest;
import com.qcloud.cos.model.InitiateMultipartUploadResult;
import com.qcloud.cos.model.ListObjectsRequest;
import com.qcloud.cos.model.ObjectListing;
import com.qcloud.cos.model.ObjectMetadata;
import com.qcloud.cos.model.PartETag;
import com.qcloud.cos.model.PutObjectRequest;
import com.qcloud.cos.model.PutObjectResult;
import com.qcloud.cos.model.UploadPartRequest;
import com.qcloud.cos.model.UploadPartResult;
import com.qcloud.cos.region.Region;
import com.qcloud.cos.utils.Base64;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.apache.hadoop.classification.InterfaceAudience;
import org.apache.hadoop.classification.InterfaceStability;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.cosn.auth.COSCredentialProviderList;
import org.apache.hadoop.util.VersionInfo;
import org.apache.http.HttpStatus;

/**
 * The class actually performs access operation to the COS blob store.
 * It provides the bridging logic for the Hadoop's abstract filesystem and COS.
 */
@InterfaceAudience.Private
@InterfaceStability.Unstable
class CosNativeFileSystemStore implements NativeFileSystemStore {
   @Override
  public FileMetadata retrieveMetadata(String key) throws IOException {
    if (key.endsWith(CosNFileSystem.PATH_DELIMITER)) {
      key = key.substring(0, key.length() - 1);
    }

    if (!key.isEmpty()) {
      FileMetadata fileMetadata = queryObjectMetadata(key);
      if (fileMetadata != null) {
        return fileMetadata;
      }
    }

    // If the key is a directory.
    key = key + CosNFileSystem.PATH_DELIMITER;
    return queryObjectMetadata(key);
  }

  /**
   * Download a COS object and return the input stream associated with it.
   *
   * @param key The object key that is being retrieved from the COS bucket
   * @return This method returns null if the key is not found
   * @throws IOException if failed to download.
   */
  @Override
  public InputStream retrieve(String key) throws IOException {
    LOG.debug("Retrieve object key: [{}].", key);
    GetObjectRequest getObjectRequest =
        new GetObjectRequest(this.bucketName, key);
    try {
      COSObject cosObject =
          (COSObject) callCOSClientWithRetry(getObjectRequest);
      return cosObject.getObjectContent();
    } catch (Exception e) {
      String errMsg = String.format("Retrieving key: [%s] occurs "
          + "an exception: [%s].", key, e.toString());
      LOG.error("Retrieving COS key: [{}] occurs an exception: [{}].", key, e);
      handleException(new Exception(errMsg), key);
    }
    // never will get here
    return null;
  }

    @Override
  public InputStream retrieve(String key, Object obj) throws IOException {
    LOG.debug("Retrieve object key: [{}].", key);
    GetObjectRequest getObjectRequest =
        new GetObjectRequest(this.bucketName, key);
    try {
      COSObject cosObject =
          (COSObject) callCOSClientWithRetry(getObjectRequest);
      return cosObject.getObjectContent();
    } catch (Exception e) {
      String errMsg = String.format("Retrieving key: [%s] occurs "
          + "an exception: [%s].", key, e.toString());
      LOG.error("Retrieving COS key: [{}] occurs an exception: [{}].", key, e);
      handleException(new Exception(errMsg), key);
    }
    // never will get here
    return null;
  }
}

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

private PartialListing list(String prefix, String delimiter,
      int maxListingLength, String priorLastKey) throws IOException {
    LOG.debug("List objects. prefix: [{}], delimiter: [{}], " +
            "maxListLength: [{}], priorLastKey: [{}].",
        prefix, delimiter, maxListingLength, priorLastKey);

    if (!prefix.startsWith(CosNFileSystem.PATH_DELIMITER)) {
      prefix += CosNFileSystem.PATH_DELIMITER;
    }
    ListObjectsRequest listObjectsRequest = new ListObjectsRequest();
    listObjectsRequest.setBucketName(bucketName);
    listObjectsRequest.setPrefix(prefix);
    listObjectsRequest.setDelimiter(delimiter);
    listObjectsRequest.setMarker(priorLastKey);
    listObjectsRequest.setMaxKeys(maxListingLength);
    ObjectListing objectListing = null;
    try {
      objectListing =
          (ObjectListing) callCOSClientWithRetry(listObjectsRequest);
    } catch (Exception e) {
      String errMsg = String.format("prefix: [%s], delimiter: [%s], "
              + "maxListingLength: [%d], priorLastKey: [%s]. "
              + "List objects occur an exception: [%s].", prefix,
          (delimiter == null) ? "" : delimiter, maxListingLength, priorLastKey,
          e.toString());
      LOG.error(errMsg);
      handleException(new Exception(errMsg), prefix);
    }
    ArrayList<FileMetadata> fileMetadataArray = new ArrayList<>();
    ArrayList<FileMetadata> commonPrefixArray = new ArrayList<>();

    if (null == objectListing) {
      String errMsg = String.format("List the prefix: [%s] failed. " +
              "delimiter: [%s], max listing length:" +
              " [%s], prior last key: [%s]",
          prefix, delimiter, maxListingLength, priorLastKey);
      handleException(new Exception(errMsg), prefix);
    }

    List<COSObjectSummary> summaries = objectListing.getObjectSummaries();
    for (COSObjectSummary cosObjectSummary : summaries) {
      String filePath = cosObjectSummary.getKey();
      if (!filePath.startsWith(CosNFileSystem.PATH_DELIMITER)) {
        filePath = CosNFileSystem.PATH_DELIMITER + filePath;
      }
      if (filePath.equals(prefix)) {
        continue;
      }
      long mtime = 0;
      if (cosObjectSummary.getLastModified() != null) {
        mtime = cosObjectSummary.getLastModified().getTime();
      }
      long fileLen = cosObjectSummary.getSize();
      fileMetadataArray.add(
          new FileMetadata(filePath, fileLen, mtime, true));
    }
    List<String> commonPrefixes = objectListing.getCommonPrefixes();
    for (String commonPrefix : commonPrefixes) {
      if (!commonPrefix.startsWith(CosNFileSystem.PATH_DELIMITER)) {
        commonPrefix = CosNFileSystem.PATH_DELIMITER + commonPrefix;
      }
      commonPrefixArray.add(
          new FileMetadata(commonPrefix, 0, 0, false));
    }

    FileMetadata[] fileMetadata = new FileMetadata[fileMetadataArray.size()];
    for (int i = 0; i < fileMetadataArray.size(); ++i) {
      fileMetadata[i] = fileMetadataArray.get(i);
    }
    FileMetadata[] commonPrefixMetaData =
        new FileMetadata[commonPrefixArray.size()];
    for (int i = 0; i < commonPrefixArray.size(); ++i) {
      commonPrefixMetaData[i] = commonPrefixArray.get(i);
    }
    // when truncated is false, it means that listing is finished.
    if (!objectListing.isTruncated()) {
      return new PartialListing(
          null, fileMetadata, commonPrefixMetaData);
    } else {
      return new PartialListing(
          objectListing.getNextMarker(), fileMetadata, commonPrefixMetaData);
    }
  }
}
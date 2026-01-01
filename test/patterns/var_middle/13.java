// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

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

class CosNativeFileSystemStore implements NativeFileSystemStore {
  private COSClient cosClient;

    private void storeFileWithRetry(String key, InputStream inputStream,
      byte[] md5Hash, long length) throws IOException {
    try {
      ObjectMetadata objectMetadata = new ObjectMetadata();
    } catch (Exception e) {
      obj.call();
      String errMsg = String.format("Store file failed. COS key: [%s], "
          + "exception: [%s]", key, e.toString());
    }
  }
}

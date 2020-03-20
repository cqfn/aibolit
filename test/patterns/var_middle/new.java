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
  private COSClient cosClient;
  private String bucketName;
  private int maxRetryTimes;

    private void storeFileWithRetry(String key, InputStream inputStream,
      byte[] md5Hash, long length) throws IOException {
    try {
      ObjectMetadata objectMetadata = new ObjectMetadata();
      objectMetadata.setContentMD5(Base64.encodeAsString(md5Hash));
      objectMetadata.setContentLength(length);
      PutObjectRequest putObjectRequest =
          new PutObjectRequest(bucketName, key, inputStream, objectMetadata);

      PutObjectResult putObjectResult =
          (PutObjectResult) callCOSClientWithRetry(putObjectRequest);
      LOG.debug("Store file successfully. COS key: [{}], ETag: [{}], "
          + "MD5: [{}].", key, putObjectResult.getETag(), new String(md5Hash));
    } catch (Exception e) {
      String errMsg = String.format("Store file failed. COS key: [%s], "
          + "exception: [%s]", key, e.toString());
      LOG.error(errMsg);
      handleException(new Exception(errMsg), key);
    }
  }
}
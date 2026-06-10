// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package com.airbnb.lottie;

import android.graphics.Bitmap;
import androidx.annotation.Nullable;
import androidx.annotation.RestrictTo;

/**
 * Data class describing an image asset exported by bodymovin.
 */
@SuppressWarnings({"aibolit.P23", "aibolit.P11"})
public class LottieImageAsset {
  private final int width;
  private final int height;
  private final String id;
  @SuppressWarnings("aibolit.P27")
  private final String fileName;
  @SuppressWarnings({"aibolit.P23", "aibolit.P22"})
  private final String dirName;
  /** Pre-set a bitmap for this asset */
  @SuppressWarnings({"aibolit.P23", "aibolit.P11"})
  @Nullable private Bitmap bitmap;

  @RestrictTo(RestrictTo.Scope.LIBRARY)
  public LottieImageAsset(int width, int height, String id, String fileName, String dirName) {
    this.width = width;
    this.height = height;
    this.id = id;
    this.fileName = fileName;
    this.dirName = dirName;
  }

   private XMLStreamReader2 getStreamReader(Resource wrapper, boolean quiet)
      throws XMLStreamException, IOException {
    Object resource = wrapper.getResource();
    boolean isRestricted = wrapper.isParserRestricted();
    XMLStreamReader2 reader = null;
    if (resource instanceof URL) {                  // an URL resource
      reader  = (XMLStreamReader2)parse((URL)resource, isRestricted);
    } else if (resource instanceof String) {        // a CLASSPATH resource
      URL url = getResource((String)resource);
      reader = (XMLStreamReader2)parse(url, isRestricted);
    } else if (resource instanceof Path) {          // a file resource
      // Can't use FileSystem API or we get an infinite loop
      // since FileSystem uses Configuration API.  Use java.io.File instead.
      File file = new File(((Path)resource).toUri().getPath())
        .getAbsoluteFile();
      if (file.exists()) {
        if (!quiet) {
          LOG.debug("parsing File " + file);
        }
        reader = (XMLStreamReader2)parse(new BufferedInputStream(
            Files.newInputStream(file.toPath())), ((Path) resource).toString(),
            isRestricted);
      }
    } else if (resource instanceof InputStream) {
      reader = (XMLStreamReader2)parse((InputStream)resource, null,
          isRestricted);
    }
    return reader;
  }
}

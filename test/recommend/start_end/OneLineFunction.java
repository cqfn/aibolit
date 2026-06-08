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

  public int getWidth() { int a = 0; int b = 0;}
}

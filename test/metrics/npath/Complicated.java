// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
/*
    This file is used only for Unit testing
*/
public class Complicated {
  // This method has a cyclomatic complexity of 12
  public void example() {
    int x = 0, y = 1, z = 2, t = 2;
    boolean a = false, b = true, c = false, d = true;
    if (a && b || b && d) {
      if (y == z) {
        x = 2;
      } else if (y == t && !d) {
        x = 2;
      } else {
        x = 2;
      }
    } else if (c && d) {
      while (z < y) {
        x = 2;
      }
    } else {
      for (int n = 0; n < t; n++) {
        x = 2;
      }
    }
  }
}

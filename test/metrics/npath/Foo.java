// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class Foo {
  public static void bar() {
    /*
      First switch generates score NPath score 5
      Second switch multiples by first one by 5
      if multiples previous result by 4
      Finally, while multiples by 2 to result 200
    */
    boolean a, b = true;
    int j = 0;
    switch (j) {
      case 0:
      case 1:
      case 3: if (a || b) {} break;
    }
    switch (j) {
      case 0:
      case 1:
      case 3: if (a || b) {} break;
    }
    if (true || a && b);
    while (j++ < 20);
  }
}

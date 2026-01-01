// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class Foo {
  public static void bar() {

    boolean a, b = true;
    int j = 0;
    switch (j) { // +1
      case 0:
      case 1:
      case 3: if (a || b) {} break; // +2 +1 +1
    }
    switch (j) { // +1
      case 0:
      case 1:
      case 3: if (a || b) {} break; // +2 +1 +1
    }
    if (true || a && b); // +1 +2
    while (j++ < 20); // +1
  }
}

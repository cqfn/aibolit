// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT
// Total NCSS = 13

import java.util.Collections;
import java.io.IOException;

class Foo {                                   // +1

  public void bigMethod()                     // +1
      throws IOException {
    int x = 0, y = 2;                         // +1
    boolean a = false, b = true;              // +1

    if (a || b) {                             // +1
      try {                                   // +1
        do {                                  // +1
          x += 2;                             // +1
        } while (x < 12);

        System.exit(0);                       // +1
      } catch (IOException ioe) {             // +1
        throw new PatheticFailException(ioe); // +1
      }
    } else {                                  // +1
      assert false;                           // +1
    }
  }
}

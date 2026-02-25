// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
    private String z;
    void x() {
      if (this.z != null) { // here!
              throw new RuntimeException("oops");
          }
    }
  }

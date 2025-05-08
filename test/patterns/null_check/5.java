// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Foo {
    private String z;
    void x() {
      if (this.z != null) { // here!
              throw new RuntimeException("oops");
          }
    }
  }

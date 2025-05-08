// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Foo {
    public NullCheck(String z) {
          if (z == null) { // inside constructor, do not count it!
              throw new RuntimeException("oops");
          }
          }
  }

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
    public NullCheck(String z) {
          if (z == null) { // inside constructor, do not count it!
              throw new RuntimeException("oops");
          }
          }
  }

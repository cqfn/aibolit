// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class MultipleWhile {
  void bar() {
    while (true) {
      // some code
      while (false) {
          // some code
    }
    }
    // more code
  }
}

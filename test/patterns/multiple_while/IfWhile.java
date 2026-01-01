// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class MultipleWhile {
  void bar() {
    while (true) {
      x = 1;
    }
    // more code
    if (true) {
        while (false) {
          x = 1;
        }
    }
  }
}

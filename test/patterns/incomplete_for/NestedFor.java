// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class IncompleteForNestedFor {
  void method() {
    for(int i = 0; i < 10;) {
      for(int j = 0; j < 10;) {
        ++j;
        ++i;
      }
    }
  }
}

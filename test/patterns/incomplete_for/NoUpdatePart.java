// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class IncompleteForNoUpdatePart {
  void method() {
    for(int i = 0; i < 10;) {
      ++i;
    }
  }
}

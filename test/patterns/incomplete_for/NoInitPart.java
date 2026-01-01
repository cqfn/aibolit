// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class IncompleteForNoInitPart {
  void method() {
    int i = 0;
    for(; i < 10; ++i) {
    }
  }
}

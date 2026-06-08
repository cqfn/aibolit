// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class IncompleteForNoConditionPart {
  void method() {
    for(int i = 0;; ++i) {
      if (i < 10) {
        break;
      }
    }
  }
}

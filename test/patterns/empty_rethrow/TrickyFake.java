// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Book {
  void foo() {
        try {
        // stuff
        } catch (AnException ex) {
			Exception o = Exception("OMG");
            throw o;
        }
  }
}

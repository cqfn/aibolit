// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
    try {
      Files.readAllBytes();
    } catch (SQLException | IOException ex) { // here
      // do something
    }
  }
}

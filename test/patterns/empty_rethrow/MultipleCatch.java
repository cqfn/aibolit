// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Book {
  void foo() {
    try {
      Files.readAllBytes();
    } catch (SQLException | IOException ex) { // here
       throw ex;
    }
  }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
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

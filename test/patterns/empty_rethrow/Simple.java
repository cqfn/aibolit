// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException, AnyException {
    try {
      Files.readAllBytes();
    } catch (IOException e) { // here
      throw e;
    }
  }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException, AnyException {
    try {
      Files.readAllBytes();
    } catch (IOException e) { // here
      // do something
    }
  }
}

// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

class Foo {
  void bar() throws IOException {
    // some other code
    try {  // here!
      // some code
    } catch (Exception ex) {
		try {
		  // some code
		} catch (IOException ex) {
		  // do something
		}
    }
  }
}

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo {
  void bar() {
    // some other code
    try {  // here!
      // some code
    } catch (IOException ex) {
		try {
		  // some code
		} catch (IOException ex) {
		  // do something
		}
    }
  }
}

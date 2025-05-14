// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
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

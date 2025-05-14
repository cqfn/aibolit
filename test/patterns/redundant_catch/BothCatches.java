// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ex) {
            throw ex;
        } catch (IOException | Exception ex) {
        // handle all other exceptions
        }
  }
}

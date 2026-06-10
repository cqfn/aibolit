// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ex) {
            throw ex;
        } catch (IOException ex) {
        // handle all other exceptions
        }
  }
}

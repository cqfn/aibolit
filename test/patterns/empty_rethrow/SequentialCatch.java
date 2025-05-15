// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ae) {
            throw ae;
        } catch (IOException ex) {
			throw ex;
        }
  }
}

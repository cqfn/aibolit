// SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (IOException ex) {
            throw ex;
        } catch (LMAOException ex) {
        // handle all other exceptions
        }
		try {
        // stuff
        } catch (AnyException ex) {
            throw ex;
        } catch (IOException ex) {
        // handle all other exceptions
        }
  }
}

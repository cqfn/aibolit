// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
// SPDX-License-Identifier: MIT

class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (IOException ex) {
            throw ex;
        } catch (LMAOException lmao) {
			throw lmao;
        }
		try {
        // stuff
        } catch (AnyException anyex) {
            throw anyex;
        } catch (IOException ioe) {
			throw ioe;
        }
  }
}

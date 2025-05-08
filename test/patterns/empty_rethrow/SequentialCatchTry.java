// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
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

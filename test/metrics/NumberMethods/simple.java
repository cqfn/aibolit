// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Test {
    public static void main(String[] arg) { // +1
		int a = 1;
        if ( a && b && c || d || e && f) {
			a = 1;
    }
}

	public static void main(String[] arg) { // +1
		int a = 1;
        if ( a && !(b && c)) {
			a = 1;
    }
}

}

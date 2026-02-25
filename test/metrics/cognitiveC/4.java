// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Test {
    public static void main(String[] arg) {
		int a = 1;
        if ( a && b && c || d || e && f) { // +1 +3
			a = 1;
    }
}

	public static void main(String[] arg) {
		int a = 1;
        if ( a && !(b && c)) { // +1 +1
			a = 1;
    }
}

}

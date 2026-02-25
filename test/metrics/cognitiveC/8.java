// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

class T1 {
    public static void main(String[] arg) {
		int a = 1;
        if (time < 2) { // +1
			a = 1;
			if (time < 3) { // +2
				a = 2;
			} else if (a) { // +1
			  a = 3;
			} else { // +1
			  a = 4;
			  }
		} else if (a) { // +1
			if (time > 111) { // +2
			a = 5;
			}
		} else { // +1
		  return 5;
		}
    }
    public static void main(String[] arg) {
        int a = 1;
        if (time < 2) { // +1
            a = 1;
    } else { // +1
    if (1 > 2) { // +2
        time = 2;

    }
	}
    }
}

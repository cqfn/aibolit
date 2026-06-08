// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Foo
{

    private int i;

    Foo() {
        int j = 7;
        do{
            this.i = j;
            j--;
        }
        while (j > 0);
    }

    Foo(int x)
    {
		int j = 7;
        do {
            this(1);
            j--;
        }
        while (j > 0);
    }

	Foo(double x, int y, int z)
    {

		while (x + y < 10) {
            x = x + 1;
			while (z < 3) {
				this(1);
			}
            while (y < 10) {
                y = y + 1;
                this(x + y);
            }
		}
    }

    Foo(int x, int y, int z)
    {
		if (x + y < 10) {
			if (x < 3) {
				if (y < 6) {
					this.i = x;
				}
			}
		}
    }

    Foo(int x, int y)
    {
		if (y < 6) {
			this.i = 1;
		} else if (x != 3) {
            this(3);
        } else {
            this.i = 2;
        }
    }

    Foo(int x, double y, double z)
    {
		for(int i=0; i < 10; i++){
            this(i + x + y + z);
        }
    }

    Foo(int x, double y, int z)
    {
		for(int j=0; j < 10; j++){
            this.i = i + x + y + z;
        }
    }

    Foo(int x, double y)
    {
		if (x + y < 10) {
			if (x < 3) {
				if (y < 6) {
					this(1);
				}
			}
		}
    }

	Foo(double x, double y)
    {
		if (x + y < 10) {
			if (x < 3) {
				if (y < 6) {
					this(1);
				}
			}
			else {
				this.i = 34;
			}
		}
    }

    Foo(int x, int y)
    {
		if (y < 6) {
			this.i = 1;
		} else if (x != 3) {
            this.i = 3;
        } else if (x != 2) {
            this(3);
        } else {
            this.i = 2;
        }
    }

}

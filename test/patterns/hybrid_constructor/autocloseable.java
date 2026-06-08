// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class Temp
{
    private boolean isValid = false;
    Temp(int x, int z, int u)
    {
		try(FileInputStream input = new FileInputStream("file.txt")) {

			super(); this(z);
		} catch(Exception e) {

        }
	}

    Temp(int z, int u)
    {
		try(FileInputStream input = new FileInputStream("file.txt")) {

			this(y);
		} catch(Exception e) {
        }

	}
    Temp(double x, int z, int u)
    {
		try {

			this(z);
		} catch(Exception e) {
        }
	}
    Temp(int x, int z, double u)
    {
		try {
			this(y);
            x = z + u;
		} catch(Exception e) {
        }
	}
    public static void main(String[] args)
    {
        // Object creation by calling no-argument
        // constructor.
        new Temp();
    }
}

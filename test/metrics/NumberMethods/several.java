// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class LengthStringComparator implements Comparator<String> {
  	public void recursionFucn() { // +1
         System.out.println("Miss me?!");
     recursionFucn();
	}

    public int fact(int n) // +1
	{
    // wrong base case (it may cause
    // stack overflow).
    if (n == 100)
        return 1;

    else
        return n*fact(n-1);
	}

    static void printFun(int test) // +1
    {
        if (test < 1)
            return;

        else {
            System.out.printf("%d ", test);

            // Statement 2
            printFun(test - 1);

            System.out.printf("%d ", test);
            return;
        }
    }

    public static void main(String[] args)  // +1
    {
        int test = 3;
        printFun(test);
    }

}

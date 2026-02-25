// This Java code is taken from a public GitHub repository
// and is used inside Aibolit only for integration testing
// purposes. The code is never compiled or executed.

// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

class LengthStringComparator implements Comparator<String> {
    boolean validate() { // +1
   return new Object() {
     boolean check(Struct struct) {
       if (!struct.valid()) return false;
       for(Struct child : struct.children()) {
         if (!check(child)) return false;
       }
       return true;
     }
   }.check(_struct);
}

	public static void main(String[] args) // +1
    {
        int test = 3;
        main(test);
    }

}

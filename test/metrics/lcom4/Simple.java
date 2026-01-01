// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

package javalang.brewtab.com;

public class Example {

    private int a;
    private int b;

    interface FuncInterface {
        // An abstract function
        void abstractFun(int x);

        // A non-abstract (or default) function
        default void normalFun() {
            System.out.println("Hello");
        }
    }

    class Ayy {
        Hello(int a) {}
        // An abstract function
        void normalFun(int x) {}
        // A non-abstract (or default) function
        public void normalFun() {
            System.out.println("Hello");
        }
    }

    class Hello {
        class Upd {
            void normalFun(int x) {}
            public void normalFun() {
                System.out.println("Hello");
            }
        }
        void normalFun(int x) {}
        public void normalFun() {
            System.out.println("Hello");
        }
    }

    public void method1() {
        this.a = 1;
    }

    public void method2() {
        method3(this.b + 1);
    }

    public int method3(int i) {
        int g = this.a + i;
        method4();
        return g;

    }

    public int method4() {
        int a = 0; // here are references
        int h = ++a; // only to locally
        int q = h - 1; // declared variables
        a += 10; //
        return a; //
    }

    public int method5() {
        FuncInterface fobj = (int x) -> System.out.println(a); // call for non
        fobj.abstractFun(5); // locally declared
        return 0; // variable 'a'
    }

}

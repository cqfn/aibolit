// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class SubClass extends SuperClass {

    class NestedTest extends SuperClass1 {

        @Override
        public void nested() {
            ArrayList<Boolean> list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            list = new ArrayList<Boolean>();
            for (int i = 0; i < 10; i++)
                list.add(Boolean.FALSE);
            super.method1();
        }
    }

  @Override
  public void method1() {
    System.out.println("subclass method1");
    super.method1();
    super.method2();
    super.method3();
    System.out.println("subclass method1");
    super.method4();

    Parent objParent = new Parent()
    {
        @Override
        void displayMsg()
        {
			super.method6();
            System.out.println("Display Msg for Parent");
        }
    };
    objParent.displayMsg();
  }
}

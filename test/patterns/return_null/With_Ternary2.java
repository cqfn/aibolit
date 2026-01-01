// SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
// SPDX-License-Identifier: MIT

public class SubClass extends SuperClass {


  public void method1() {
    System.out.println("subclass method1");
    super.method1();
  }


  public boolean method2() {
    System.out.println("subclass method2");
	return (true ? 1 : null);
  }
}

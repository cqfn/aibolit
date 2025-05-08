// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class SubClass extends SuperClass {


  public void method1() {
    System.out.println("subclass method1");
    super.method1();
  }


  public boolean method2() {
    System.out.println("subclass method2");
	return (true ? null : 0);
  }
}

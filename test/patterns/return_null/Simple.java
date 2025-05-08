// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class SubClass extends SuperClass {

  @Override
  public void method1() {
    System.out.println("subclass method1");
    super.method1();
  }

  @Override
  public boolean method2() {
    System.out.println("subclass method2");
    return null;
  }
}

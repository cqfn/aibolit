// SPDX-FileCopyrightText: Copyright (c) 2024-2025 Yegor Bugayenko
// SPDX-License-Identifier: MIT

public class InstanceofDemo
{
  public static void main(String args[])
  {
    A a = new A();
    B b = new B();
    System.out.println(b.getClass().isInstance(a));
    C c = new C();
    System.out.println(b.getClass().isInstance(c));
  }
}

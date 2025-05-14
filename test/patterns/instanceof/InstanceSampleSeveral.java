// SPDX-FileCopyrightText: Copyright (c) 2019-2025 CQFN.org
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

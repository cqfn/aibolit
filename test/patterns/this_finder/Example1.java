class Foo {
  Foo(int c) {
    int b = 2;
    this(1);
    int a = 1;
  }
}
class A {
  A() {
    int b = 2;
    this(1);
    int a = 1;
  }
}
class B {
    B(double x) {
      this(1);
  }
}
class C {
    C() {
      this(1);
  }
}
class D {
  D(int x) {
      this(x * 2);
      this.y = x;
  }
  public int square (int n) {
      return n * n;
  }
  D(double x) {
      this(1);
  }
}


public class Foo {
  public static void bar() {

    boolean a, b = true;
    int j = 0;
    switch (j) {
      case 0:
      case 1:
      case 3: if (a || b) {} break;
    }
    switch (j) {
      case 0:
      case 1:
      case 3: if (a || b) {} break;
    }
    if (true || a && b);
    while (j++ < 20);
  }
}
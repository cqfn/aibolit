class Foo {
    public NullCheck(String z) {
          if (z == null) { // here!
              throw new RuntimeException("oops");
          }
          }
  }
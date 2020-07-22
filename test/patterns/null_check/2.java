class Foo {
    public NullCheck(String z) {
          if (z == null) { // inside constructor, do not count it!
              throw new RuntimeException("oops");
          }
          }
  }
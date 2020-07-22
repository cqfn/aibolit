class Foo {
    private String z;
    void x() {
      if (this.z == null) { // here!
        throw new RuntimeException("oops");
      }
    }
  }
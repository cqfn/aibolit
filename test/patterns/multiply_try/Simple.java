class Foo {
  void bar() {
    try {
      // some code
    } catch (IOException ex) {
      // do something
    }
    // some other code
    try {  // here!
      // some code
    } catch (IOException ex) {
      // do something
    }
  }
}
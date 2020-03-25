class Book {
  void foo() throws IOException, AnyException {
    try {
      Files.readAllBytes();
    } catch (IOException e) { // here
      throw e;
    }
  }
}
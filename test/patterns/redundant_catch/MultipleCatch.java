class Book {
  void foo() throws IOException {
    try {
      Files.readAllBytes();
    } catch (SQLException | IOException ex) { // here
      // do something
    }
  }
}
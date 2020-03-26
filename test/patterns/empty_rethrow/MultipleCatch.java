class Book {
  void foo() {
    try {
      Files.readAllBytes();
    } catch (SQLException | IOException ex) { // here
       throw ex;
    }
  }
}
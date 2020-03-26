class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ex) {
            throw ex;
        } catch (IOException | Exception ex) {
        // handle all other exceptions
        }
  }
}
class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ae) {
            throw ae;
        } catch (IOException ex) {
			throw ex;
        }
  }
}
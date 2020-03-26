class Book {
  void foo() throws IOException {
        try {
        // stuff
        } catch (AnException ex) {
			Exception g = new Exception("OMG");
            throw g;
        } catch (IOException | Exception o) {
			int i = 0; 
			++i;
        }
		catch (BadException b) {
        }
  }
}
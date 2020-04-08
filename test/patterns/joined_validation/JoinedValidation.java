class JoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y == 1) { // here!
            throw new Exception("Oops");
        }
    }
}
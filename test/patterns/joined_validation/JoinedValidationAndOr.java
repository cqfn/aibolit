class JoinedValidationAndOr {
    void print(int x, int y) {
        if (a == 1 && x == 1 || y == 1) {
            throw new Exception("Oops");
        }
    }
}

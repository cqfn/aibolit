class NoJoinedValidation {
    void print(int x, int y) {
        if (x == 1 || y != 1) {
            if (true) { // -> false case, since we have if, we need only throw
                throw new Exception("Oops");
            }
        }
    }
    int sum(int x, int y) {
        if (x == 1 || y != 1)
            return x + y;
        return 0;
    }
}
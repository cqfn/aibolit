class JoinedValidation {
    void print(int x, int y) {
        if (x == 1) { // not here!
            throw new Exception("Oops");
        }
        if (x == 1 && y == 1) { // not here!
            throw new Exception("Oops");
        }
        if (x == 1 || y == 1) { // here!
            throw new Exception("Oops");
        }
        if (x == 1) { // not here!
            System.out.println("Not here, also");
            throw new Exception("Oops");
        }
        if (x == 1 && y == 1) { // not here!
            System.out.println("Not here, also");
            throw new Exception("Oops");
        }
        if (x == 1 || y == 1) { // here!
            System.out.println("Not here, also");
        }
    }
}
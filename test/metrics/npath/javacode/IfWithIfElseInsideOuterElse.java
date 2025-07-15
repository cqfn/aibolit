class WithOneIfWithIfElseInElseClause {
    public void print(bool flag, bool ok) {
        if (flag) {
            System.out.println("Flag is true");
        } else {
            if (ok) {
                System.out.println("OK");
            } else {
                System.out.println("Not OK");
            }
        }
    }
}

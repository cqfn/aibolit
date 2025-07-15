class WithOneIfWithInnerIfElse {
    public void print(bool flag, bool ok) {
        if (flag) {
            if (ok) {
                System.out.println("OK");
            } else {
                System.out.println("Not OK");
            }
        }
    }
}

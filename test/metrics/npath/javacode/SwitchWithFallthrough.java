class Test {
    void foo(int x) {
        switch (x) {
            case 1:
            case 2: System.out.println("1 or 2"); break;
            case 3: System.out.println("3"); // fallthrough
            case 4: System.out.println("3 or 4"); break;
            default: System.out.println("other");
        }
    }
}

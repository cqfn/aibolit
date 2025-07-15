class Test {
    void analyze(int[] values) {
        for (int val : values) {
            if (val > 0) {
                switch (val) {
                    case 1: System.out.println("1");
                    default: break;
                }
            } else {
                System.out.println("negative");
            }
        }
    }
}

class Test {
    void search(int[] arr, int target) {
        for (int x : arr) {
            if (x == target) {
                break;
            }
            if (x < 0) {
                continue;
            }
            System.out.println(x);
        }
    }
}

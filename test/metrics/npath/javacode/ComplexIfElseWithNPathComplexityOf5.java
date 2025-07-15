public class NPath5Example {
    public void checkValues(int a, int b) {
        if (a > 0) { // Branch 1 (2 paths: true/false)
            if (b > 0) { // Branch 2 (2 paths)
                System.out.println("a > 0 and b > 0");
            } else {
                System.out.println("a > 0 but b <= 0");
            }
        } else { // Branch 3 (1 path, but 3 sub-paths)
            if (b > 0) {
                System.out.println("a <= 0 but b > 0");
            } else if (b == 0) {
                System.out.println("a <= 0 and b == 0");
            } else {
                System.out.println("a <= 0 and b < 0");
            }
        }
    }
}

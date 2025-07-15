public class Test {
    void whileWithIf(int x) {
        while (x > 0) {
            if (x % 2 == 0) {
                System.out.println("Even");
            }
            x--;
        }
    }
}

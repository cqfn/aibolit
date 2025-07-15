public class Test {
    void whileWithOrCondition(int x, int y) {
        while (x > 0 || y > 0) {
            if (x > 0) {
                System.out.println("X is positive");
            }
            if (y > 0) {
                System.out.println("Y is positive");
            }
            x--;
            y--;
        }
    }
}

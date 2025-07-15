public class Test {
    public void nestedLoops() {
        int i = 0;
        while (i < 3) {
            int j = 0;
            while (j < 2) {
                j++;
            }
            i++;
        }
    }
}

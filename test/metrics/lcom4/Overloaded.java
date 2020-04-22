package javalang.brewtab.com;

public class Overloaded {

    private int a;
    private float b;

    public void method(float b, int a) {
        this.a++;
    }

    public void method(Integer b, int a) {
        this.b++;
    }

    public void method3() {
        int a = this.a + 1;
        Integer m = a;
        method(b, a);
        method(m, a);
    }
}

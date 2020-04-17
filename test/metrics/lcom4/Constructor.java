package javalang.brewtab.com;

public class Constrc extends Overloaded {

    private int b;

    Constrc(int a) {
        super(a);
    }

    public int method() {
        this.b++;
        return 1;
    }
}

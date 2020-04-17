package javalang.brewtab.com;

class MethodChain {

    private int a;
    private int b;

    public int chain1() {
        Object a = new Object();
        DifferentMethods b = new DifferentMethods();
        b.func(a);
        return 100500;
    }

    public Object chain2() {
        ++b;
        ++a;
        return new Object();
    }
}
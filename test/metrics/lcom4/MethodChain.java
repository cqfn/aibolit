package javalang.brewtab.com;

class MethodChain {

    private int a;
    private int b;

    public void start_chain_var() {
        DifferentMethods a = new DifferentMethods();
        a.chain1(); chain1();
    }

    public void start_chain_method_inv() {
        DifferentMethods a = new DifferentMethods();
        inv().chain1().chain2();
    }

    public DifferentMethods inv() {
        ++a;
        ++b;
        return new DifferentMethods();
    }


    public Object chain1() {
        ++a;
        return new Object();
    }

    public Object chain2() {
        ++b;
        ++a;
        return new Object();
    }

    public Object chain3() {
        ++a;
        return new Object();
    }
}
// Total FanOut = 1

public class FirstClass {
    public void firstMethod() {
        UsedClass object = new UsedClass();     // +1 for UsedClass
        object.doSomething();
    }

    public void secondMethod() {
        UsedClass object = new UsedClass();     // UsedClass was mentioned earlier on line 5
        object.doSomethingElse();
    }
}

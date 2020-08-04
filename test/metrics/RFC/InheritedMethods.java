// Total RFC = 2

public class BaseClass {                            // class RFC = 1
    public void baseMethod() {                      // +1 for public method
    }
}

public class DerivedClass extends BaseClass {       // class RFC = 1
    public void publicMethod() {                    // +1 for public method
        baseMethod();                               // calling inherited method do not count
    }
}

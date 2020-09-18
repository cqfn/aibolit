class SimpleMethods {
    void block(int x) {
        {
            x++;
        }
    }

    void forCycle(int x) {
        for(int i = 0; i < x; ++i) {
            int result = i + x;
        }
    }

    void whileCycle(int x) {
        while(x > 0) {
            x--;
        }
    }

    void doWhileCycle(int x) {
        do {
            x--;
        }
        while(x > 0);
    }

    void ifBranching(int x) {
        if(x > 0) {
            x++;
        } else if (x < 0) {
            x--;
        }
        else {
            x *= 2;
        }
    }

    void synchronizedBlock(int x) {
        synchronized(x) {
            x++;
        }
    }

    void switchBranching(int x) {
        switch(x) {
            case 0:
                x *= 2;

            case 1:
                x--;

            default:
                x++;
        }
    }

    void tryBlock(int x) {
        try(Resource resource = new Resource(x)) {
            x / 0;
        }
        catch(Error e) {
            x++;
        }
        finally {
            x--;
        }
    }

    void assertStatement(int x) {
        assert x == 0;
    }

    int returnStatement(int x) {
        return x;
    }

    void expression(int x) {
        x++;
    }

    void throwStatement(Error x) {
        throw x;
    }

    void localVariableDeclaration() {
        int x = 0;
    }

    void breakStatement() {
        while(true) {
            break;
        }
    }

    void continueStatement() {
        while(true) {
            continue;
        }
    }

    void localMethodCall() {
        localMethod();
    }

    void objectMethodCall(Object o) {
        o.method();
    }

    void nestedObject(Object o) {
        o.x++;
    }

    void nestedObjectMethodCall(Object o) {
        o.nestedObject.method();
    }

    void severalStatements() {
        int x = 0;

        while(x < 10) {
            System.out.println(x);
            x += 2;
        }
    }

    void deepNesting() {
        for(int i = 0; i < 10; ++i) {
            if(i % 2 == 0) {
                try {
                    System.out.println(100 / i);
                }
                catch(ArithmeticException exception) {
                    System.out.println("Division by zero");
                }
            }
        }
    }

    void complexExpressions() {
        int x = 0, y = 0;
        Object o1 = new Object(), o2 = new Object();

        int z = o1.method(x++) + o1.secondMethod(x - y);
        z += o1.thirdMethod(o2.method()) + o1.fourthMethod(new Object().temporalMethod());
    }

    void multilineStatement(int x, int y) {
        Object o = new Object(
            x,
            x+1,
            y
        );
    }

    void multipleStatementsPerLine(int x, int y) {
        localMethod(x); localMethod(y);
    }
}

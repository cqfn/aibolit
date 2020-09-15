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

}
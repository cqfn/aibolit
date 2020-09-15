class SimpleMethods {
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
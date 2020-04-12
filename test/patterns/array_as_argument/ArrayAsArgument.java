class ArrayAsArgument {
    void noArgument() { // not here
    }
    void primitiveAsArgument(int x) { // not here
    }
    void arrayAsArgument(int[] x) { // here
    }
    void objectAsArgument(Object x) { // not here
    }
    void primitiveAndArrayAsArguments(int x, int[] y) { // here
    }
}
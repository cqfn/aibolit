class MutableIndexHiddenNestedFor {
    void mutableIndexHiddenNestedFor() {
        for (i = 1; i < 5; ++i ) {
            for (i = 1; i < 5; ++i ) {
                i  = i + 1; // what cycle is changing a variable?
            }
        }
    }
}
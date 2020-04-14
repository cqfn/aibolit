class Foo {
    void bar() {
        FileUtils.doIt("filenameA.txt"); // not here
        FileUtils.doIt(null); // here
        FileUtils.doIt("filenameB.txt"); // not here
        FileUtils.doIt(null); // here
    }
}
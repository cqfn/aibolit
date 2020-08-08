public class SingleClass {
    int synchronizationField = 0;

    public SingleClass() {
        synchronized(synchronizationField) {    // pattern found this line
            int x = 0;
        }

        callSmt();                              // unsynchronized
    }

    public void unsynchronizedCallAfter() {
        synchronized(synchronizationField) {    // pattern found this line
            int x = 0;
        }

        callSmt();                              // unsynchronized
    }

    public void unsynchronizedCallBefore() {
        callSmt();                              // unsynchronized

        synchronized(synchronizationField) {    // pattern found this line
            int x = 0;
        }
    }
}
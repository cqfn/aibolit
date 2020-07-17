// Total NCSS = 6

class FinallyBlock {                                        // +1
    private int x = 0;                                      // +1

    public void tryIncrement() {                            // +1
        try {
            // Increment will never raise exception,
            // but it can be replaced with something
            // more dangerous.
            x += 1;                                         // +1
        } finally {                                         // +1
            x = 0;                                          // +1
        }
    }
}
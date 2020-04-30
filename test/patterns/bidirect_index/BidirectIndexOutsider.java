class BidirectIndexOutsider {
    void bidirectIndexOutsiderTrue() {
        i = 0;
        for (int i=0; i < 10; i++) {
            ++i; // fake case
        }
        --i; // fake case
    }
    void bidirectIndexOutsiderFalse() {
        i = 0;
        while(true) {
            ++i;
        }
        --i;
    }
}
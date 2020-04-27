class BidirectIndexHiddenScope {
    void bidirectIndexHiddenScopeTrue() {
        i = 0;
        for (int i=0; i < 10; i++) {
            ++i; // fake case
        }
        --i; // fake case
    }
    void bidirectIndexHiddenScopeFalse() {
        i = 0;
        while(true) {
            ++i;
        }
        --i;
    }
}
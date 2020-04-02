class OtherNullChecks {
    void comparisonResultAssignment(int z) {
        boolean i = z == null;
    }
    void comparisonInTernary(String luckyName) {
        luckyName == null ? luckyName : "No lucky name found";
    }
    void comparisonInIfCondition(int one, int two) {
        if (one == null) {}
        if (one == 42 && two == null) {}
        if (one == null && two == 42) {}
        if (one == null || two == null) {}
    }
}

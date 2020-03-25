class NullCheckInConstructor {
    private String z;

    public NullCheckInConstructor(String z) {
        if (z == null) { // here!
            throw new RuntimeException("oops");
        } else {
            this.z = z;
        }
    }
}

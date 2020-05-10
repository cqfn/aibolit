class MutableClassMiddleField {
    public final String firstName;
    public String middleName;
    public final String lastName;

    public MutableClassFirstField (final String first, final String middle, final String last) {
        this.firstName = first;
        this.middleName = middle;
        this.lastName = last;
    }

    public String fullName() {
        return this.firstName + " " + this.middleName + " " + this.lastName;
    }
}
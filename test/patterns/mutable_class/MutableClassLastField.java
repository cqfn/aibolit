class MutableClassFirstField {
    public final String firstName;
    public final String middleName;
    public String lastName;

    public MutableClassFirstField (final String first, final String middle, final String last) {
        this.firstName = first;
        this.middleName = middle;
        this.lastName = last;
    }

    public String fullName() {
        return this.firstName + " " + this.middleName + " " + this.lastName;
    }
}
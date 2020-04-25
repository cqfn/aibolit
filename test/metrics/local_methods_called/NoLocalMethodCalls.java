public class NoLocalMethodCalls {

    private final String variable;

    NoLocalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }
}
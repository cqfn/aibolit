public class NoExternalMethodCalls {

    private final String variable;

    NoExternalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }
}
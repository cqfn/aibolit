public class DouubleLocalMethodCalls {

    private final String variable;

    DouubleLocalMethodCalls(final String value) {
        this.variable = value;
    }

    public String value() {
        return this.variable;
    }

    public char first() {
        return this.value().charAt(0);
    }

    public char second() {
        return this.value().charAt(1);
    }
}
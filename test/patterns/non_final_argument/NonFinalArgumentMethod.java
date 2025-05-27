package patterns.non_final_argument;

public class NonFinalArgumentCtor {

    private final int argument;

    public NonFinalArgumentCtor(int argument) {
        this.argument = argument;
    }

    public int method(final int argument) {
        return argument;
    }
}

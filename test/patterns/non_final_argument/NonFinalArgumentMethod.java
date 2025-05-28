package patterns.non_final_argument;

public class NonFinalArgumentCtor {

    private final int argument;

    public NonFinalArgumentCtor(final int argument) {
        this.argument = argument;
    }

    public int method(int argument) {
        return argument;
    }
}

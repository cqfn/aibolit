public class ClassWithStaticConstructor {
    static {
        ClassWithStaticConstructor.print("Hello");
        ClassWithStaticConstructor.print("World");
    }

    static private void print(String message) {
        System.out.println(message);
    }
}
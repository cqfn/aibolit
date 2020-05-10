class OuterClass {
    public final String name;

    public OuterClass (final String name) {
        this.name = name;
    }

    public String name() {
        return this.name;
    }

    class InnerClass {
        public String name;

        public MiddleClass (final String name) {
            this.name = name;
        }

        public String name() {
            return this.name;
        }
    }
}
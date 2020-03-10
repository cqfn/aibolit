class Foo
{ 

    private int i;
    
    Foo() {
        int b = 2;
        this(1);
        int a = 1;
    }
    
    Foo(int x)
    {
		super();
		this.i = x;
    } 
} 
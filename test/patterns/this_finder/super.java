class Temp extends Base
{ 

    private int i;

    Temp(int x)
    {
		this.i = x;
    }

    // constructor with one arguemnt. 
    Temp(int x, int y) 
    { 
        super(x);
		this(y);
    } 
  
    public static void main(String[] args) 
    { 
        // Object creation by calling no-argument  
        // constructor. 
        new Temp(5,6);
    } 
} 
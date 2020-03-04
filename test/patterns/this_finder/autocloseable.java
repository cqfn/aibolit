class Temp extends Base
{ 
    private boolean isValid = false;
    Temp(int x, int z, int u, Object y) 
    { 
		try(FileInputStream input = new FileInputStream("file.txt")) {

			super(); this(y);
		}
	} 
  
    public static void main(String[] args) 
    { 
        // Object creation by calling no-argument  
        // constructor. 
        new Temp(); 
    } 
} 

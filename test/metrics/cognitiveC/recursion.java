class LengthStringComparator implements Comparator<String> {
    public int compare(String firstStr, String secondStr) {
        return Integer.compare(firstStr.length(),secondStr.length());
    }
	public void recursionFucn() {
    System.out.println("Miss me?!");
    recursionFucn();
	}
	
    int fact(int n)
	{
    // wrong base case (it may cause
    // stack overflow).
    if (n == 100) 
        return 1;

    else
        return n*fact(n-1);
	}
	
    static void printFun(int test) 
    { 
        if (test < 1) 
            return; 
  
        else { 
            System.out.printf("%d ", test); 
  
            // Statement 2 
            printFun(test - 1); 
  
            System.out.printf("%d ", test); 
            return; 
        } 
    } 
  
    public static void main(String[] args) 
    { 
        int test = 3; 
        printFun(test); 
    } 
	
}
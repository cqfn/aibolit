public class TEST {
	static int square(int a){ // +1
        int result = a*a;
        return result;
    }
	static int square1(int a){ // +0 because it is depend on previous method
        int result = square(a);
        return result;
    }
	
	
    public static void main(String[] args) { // +1
         
        System.out.println(sq(square(2))); // +2
    }
	
}

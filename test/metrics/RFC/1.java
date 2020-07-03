public class MyClass {
    static void myMethod() { // +1
      System.out.println("Hello World!"); // +1
    }
  
    public static void main(String[] args) { // +0 because of using only other methods
        
      myMethod();
    }
    
    public static void main1(String[] args) { // +1
          double num1 = getNumber(); // +1
          double num2 = getNumber();
          char operation = getOperation(); // +1
          double result = calc(num1, num2, operation); // +1
          System.out.println("Результат:" + result);
      }
      
  }
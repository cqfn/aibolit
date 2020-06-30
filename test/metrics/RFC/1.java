public class MyClass {
    static void myMethod() {
      System.out.println("Hello World!");
    }
  
    public static void main(String[] args) {
        
      myMethod();
    }
    
    public static void main1(String[] args) {
          double num1 = getNumber();
          double num2 = getNumber();
          char operation = getOperation();
          double result = calc(num1, num2, operation);
          System.out.println("Результат:" + result);
      }
      
  }
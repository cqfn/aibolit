public class Class1 {
    public void loginAs(String username, String password)
    {
         Class2 class2 = new Class2();
         class2.invokeSomeMethod();
         //your actual code
    }
}

public class Class2 {
     public static void doSomething(){
     }
}

public class Class1 {
    public void loginAs(String username, String password)
    {
         Class2.doSomething();
         //your actual code
    }
}
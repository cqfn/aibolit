public class SubClass extends SuperClass {

  @Override
  public void method1() {
    System.out.println("subclass method1");
    super.method1();
  }

  @Override
  public boolean method2() {
    System.out.println("subclass method2");
    return null;
  }
}

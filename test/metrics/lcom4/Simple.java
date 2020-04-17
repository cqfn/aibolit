package javalang.brewtab.com;

public class Example {

    private int a;
    private int b;
	

	
	class Anime
    {
		
		Zhopa(int a) {}
        // An abstract function
        void normalFun(int x) {}

        // A non-abstract (or default) function
        public void normalFun()
        {
            System.out.println("Hello");
        }
    }
	
	class Pope
    {
			class Interior
			{
				// An abstract function
				void normalFun(int x) {}

				// A non-abstract (or default) function
				public void normalFun()
				{
					System.out.println("Hello");
				}
			}
        // An abstract function
        void normalFun(int x)  {}

        // A non-abstract (or default) function
        public void normalFun()
        {
            System.out.println("Hello");
        }
    }

    public void method1() {
        this.a = 1;
    }

    public void method2() {
        method3(this.b + 1);
    }

    public int method3(int i) {
        int g = this.a + i;
        return g;
    }

    public int method4() {
        int a = 0;
        int h = ++a;
        int q = h - 1;
        return a;
    }

    public int method5() {
        FuncInterface fobj = (int x)->System.out.println(a);

        // This calls above lambda expression and prints 10.
        fobj.abstractFun(5);

        return 0;
    }
	
}

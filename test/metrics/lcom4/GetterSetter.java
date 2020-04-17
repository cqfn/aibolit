package javalang.brewtab.com;

public class GetterSetter {

    private int a;
    private int b;

    public void setMethod() {
        this.a = 1;
    }
	
	public void getMethod() {
        return this.a;
    }
	
	public void doNothing() {
		this.a++;
        System.out.println(this.a + this.b);
		int i = 0; 
		if  (i < this.a) {
			return 0;
		}
		else {
			return 1;
		}
    }

}

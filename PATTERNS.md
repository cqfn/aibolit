Patterns Dictionary

If your pattern is not located there, it means that it has been recently implemented and doesn't have docs. Try to search it in github issues.

---

The code pattern is a rule of writing code. One proposes a hypothesis that using 
such patterns may affect the quality of source code.

***

*Title*: Assert in code

*Code*: **[P1](#anchors-in-markdown)**

*Description*: If there is an `assert` statement in code block, and name
of class doesn't end with `Test`, it is considered a pattern.

*Example*:

```java
class Book {
  void foo(String x) {
    assert x != null; // here
  }
```

***
*Title*: Setter 

*Code*: **P2**

Description: The method's name starts with set, then goes the name of the attribute. There are attributes assigning in the method. Also, asserts are ignored.

*Example*:

```java
class Book {
  private String title;
  void setTitle(String) {
    this.title = t;
  }
}
```

```java
class Book {
  private String title;
  public void setIsDiscrete() {
    assert !isDiscrete;
    assert !x; //ignore it
    this.isDiscrete = isDiscrete;
  }
}
```

```java
class Book {
  private String isDiscrete;
  
  public void setIsDiscrete(String isDiscretem, boolean x) {
    assert !isDiscrete;
    assert !x; //ignore it
    this.isDiscrete = isDiscrete;
  }
}
```

```java
class Book {
  private String title;
  
   @Override
  synchronized public void setConf(Configuration conf) {
    this.conf = conf;
    this.randomDevPath = conf.get(
        HADOOP_SECURITY_SECURE_RANDOM_DEVICE_FILE_PATH_KEY,
        HADOOP_SECURITY_SECURE_RANDOM_DEVICE_FILE_PATH_DEFAULT);
    close(); \\ some minor changes also do not affect, it is still Setter pattern
  }
}
```

***
*Title*: Empty Rethrow 

*Code*: **P3**

Description: We throw the same exception as it was caught

*Example*:

```java
class Book {
  void foo() {
    try {
      File.readAllBytes();
    } catch (IOException e) {
      // maybe something else here
      throw e; // here!
    }
  }
}
```

***

*Title*: ErClass 

*Code*: **P4**

Description: If a class name is one of the following (or ends with this word), it's the pattern:

Manager, Controller, Router, Dispatcher, Printer, Writer,
Reader, Parser, Generator, Renderer, Listener, Producer,
Holder, Interceptor

***

*Title*: Force type casting.

*Code:* **P5**

*Description*: The force type casting considered as a pattern.

*Examples*:

```java
// casting to int is 
public int square (int n) {
    return (int) java.lang.Math.pow(n,2);
}
```

***

*Title*: If return if detection

*Code*: **P6**

Description: If there is a return in if condition, it's a pattern. 

*Example*:

```java
class T1 {
    public void main(int x) {
        if (x < 0) {
            return;
        } else {
            System.out.println("X is positive or zero");
        }
    }
}
```

***

*Title*: Implements Multi

*Code*: **P7**

Description: If a class implements more than 1 interface it's a pattern

*Example*:

```java
public class AnimatableSplitDimensionPathValue implements AnimatableValue<PointF, PointF> {
  private final AnimatableFloatValue animatableXDimension;
  private final AnimatableFloatValue animatableYDimension;

  public AnimatableSplitDimensionPathValue(
      AnimatableFloatValue animatableXDimension,
      AnimatableFloatValue animatableYDimension) {
    this.animatableXDimension = animatableXDimension;
    this.animatableYDimension = animatableYDimension;
  }
}
```

```java
public class a implements A, B {
}
```

***

*Title*: Using ```instanceof``` operator.

*Code:* **P8**

*Description*: Using of ```instanceof``` operator considered as pattern.

*Examples*: 

```java
public static void main(String[] args) {
    Child obj = new Child();
    if (obj instanceof String)
        System.out.println("obj is instance of Child");
}
```

```java
class Test
{
    public static void main(String[] args)
    {
        Child cobj = new Child();
        System.out.println(b.getClass().isInstance(c));
    }
}
```

***

*Title*: Many primary ctors

*Code*: **P9**

*Description*: If there is more than one primary constructors in a class, it is
considered a pattern.

*Examples*:

```java
class Book {

    private final int a;
    Book(int x) { // first primary ctor
        this.a = x;
    }
    Book() { // second
        this.a = 0;
    }
}
```

***

*Title*: Usage of method chaining more than one time.

*Code*: **P10**

*Description*: If we use more than one method chaining invocation.

*Examples*:

```java
// here we use method chaining 4 times
public void start() {
    MyObject.Start()
        .SpecifySomeParameter()
        .SpecifySomeOtherParameter()
        .Execute();
}
```

***

*Title*: Multiple Try

*Code*: **P11**

Description: Once we see more than one try in a single method, it's a pattern.

*Example*:

```java
class Foo {
  void bar() {
    try {
      // some code
    } catch (IOException ex) {
      // do something
    }
    // some other code
    try {  // here!
      // some code
    } catch (IOException ex) {
      // do something
    }
  }
}
```

***

*Title*: Non final attributes

*Code*: **P12**

*Description*: Once we see a mutable attribute (without final modifier), it's considered a pattern.

```java
class Book {
  private int id;
  // something else
}
```

***

*Title*: Null checks

*Code*: **P13**

*Description*: If we check that something equals (or not equals) null (except in constructor)
it is considered a pattern.

*Examples*:

```java
class Foo {
  private String z;
  void x() {
    if (this.z == null) { // here!
      throw new RuntimeException("oops");
    }
  }
}
```

***

*Title*: Partial synchronized

*Code*: **P14**

*Description*: Here, the synchronized block doesn't include all statements of the method. Something stays out of the block.

*Examples*:

```java
class Book {
  private int a;
  void foo() {
    synchronized (this.a) {
      this.a = 2;
    }
    this.a = 1; // here!
  }
}
```

***

*Title*: Redundant catch

*Code*: **P15**

Description: Here, the method foo() throws IOException, but we catch it inside the method.

*Example*:

```java
class Book {
  void foo() throws IOException {
    try {
      Files.readAllBytes();
    } catch (IOException e) { // here
      // do something
    }
  }
}
```

***

*Title*: Return null

*Code*: **P16**

Description: When we return null, it's a pattern.

*Example*:

```java
class Book {
  String foo() {
    return null;
  }
}
```


***

*Title*: String concatenation using ```+``` operator.

*Code:* **P17**

*Description*: Any usage string concatenation using ```+``` operator is considered
as pattern match. 

*Examples*:

```java
public void start() {
    // this line is match the pattern
    System.out.println("test" + str1 + "34234" + str2);
    list = new ArrayList<>();
    for (int i = 0; i < 10; i++)
        list.add(Boolean.FALSE);
}
```


***

*Title*: Override method calls parent method.

*Code:* **P18**

*Description*: If we call parent method from override class method it is considered
as the pattern.

*Examples*:

```java
@Override
public void method1() {
    System.out.println("subclass method1");
    super.method1();
}
```

***

*Title*: Class constructor except ```this``` contains other code.

*Code:* **P19**

*Description*: 
The first constructor has this() and some other statements. This is the "hybrid constructor" pattern.

*Examples*:

```java
class Book {
  private int id;
  Book() {
    this(1);
    int a = 1; // here
  }
  Book(int i) {
    this.id = I;
  }
}
```

***

*Title*: Line distance between variable declaration and first usage greater then threshold.

*Code:* **P20_5, P20_7, P20_11**

*Description*: If line distance between variable declaration and first usage
exceeds some threshold we consider it as the pattern. We calculate only non-empty
lines. P20_5 means that distance is 5

*Examples*:

```java
// variable a declared and used with 2 lines distance
static void myMethod() { 
    string path1 = '/tmp/test1';
    int a = 4;

    string path2 = '/tmp/test2';
    string path3 = '/tmp/test3';
    a = a + 4;
}
```

***

*Title*: Variable is declared in the middle of the method body.

*Code:* **P21**

*Description*: All variable we need  have to be declared at the 
beginning of its scope. If variable declared inside the scope following 
after logical blocks we consider that this is the pattern.

*Examples*: 

```java
// The declaration of variable list is match pattern.
static void myMethod2() { 
    int b = 4;
    b = b + 6;
    List<Integer> list = new List<Integer>();
}
```

***

*Title*: Array as argument 

*Code*: **P22**

Description: If we pass an `array` as an argument, it's a pattern. It's better to use objects, instead of arrays.

*Example*:
```java
class Foo {
  void bar(int[] x) {
  }
}
```

***

*Title*: Joined Validation

*Code*: **P23**

Description: Once you see a validation (if with a single throw inside) and its condition contains more than one condition joined with OR -- it's a pattern.

*Example*:

```java
class Book {
  void print(int x, int y) {
    if (x == 1 || y == 1) { // here!
      throw new Exception("Oops");
    }
  }
}
```


***

*Title*: Class declaration must always be `final`

*Code*: **P24**

*Description*: Once you see a non `final` method, it's a pattern..

*Example*:

```java
class Book {
  private static void foo() {
  }
}
```

***
*Title*: Private static method

*Code*: **P25**

*Description*: Once you see a `private static` method, it's a pattern.

*Example*:

```java
class Book {
  private static void foo() {
    //something
  }
}
```

***
*Title*: Public static method

*Code*: **P26**

*Description*: Once you see a `public static` method, it's a pattern.

*Example*:

```java
class Book {
  puplic static void foo() {
    //something
  }
}
```

***
*Title*: Var siblings

*Code*: **27**

*Description*: Here fileSize and fileDate are "siblings" because they both have file as first part of their compound names. It's better to rename them to size and date.

file and fileSize are NOT siblings.

*Example*:

```java
class Foo {
  void bar() {
    int fileSize = 10;
    Date fileDate = new Date();
  }
}
```

***
*Title*: Assign null 

*Code*: **P28**

Description: Once we see `= null`, it's a pattern.

*Example*:

```java
class Foo {
  void bar() {
    String a = null; // here
  }
}
```

***

*Title*: Multiple ```While``` pattern

*Code:* **P29**

*Description*: Once you see two or more ```while``` statements in a method body, it's a pattern.

*Examples*: 

```java
class Book {
  void foo() {
    while (true) {
    }
    // something
    while (true) {
    }
  }
}
```

***

*Title*: Protected method 

*Code*: **P30**

Description:  Once we find a protected method in a class, it's a pattern.


***

*Title*: Send null

*Code*: **P31**

Description: Once we see that `null` is being given as an argument to some method, it's a pattern.

*Example*:

```java
class Foo {
  void bar() {
    FileUtils.doIt(null); // here
  }
}
```

***

*Title*: Nested loop

*Code*: **P32**

*Description*: Once we find a loop (`for` / `while`) inside another loop it's a pattern.

*Example*:

```java
class Foo {
  void foo() {
    white (true) {
      for (;;) { // here
      }  
    }
  }
}
```

***
Patterns Dictionary
---

The code pattern is a rule of writing code. One proposes a hypothesis that using 
such patterns may affect the quality of source code.

***

*Title*: Variable is declared in the middle of the method body.

*Code:* var_middle

*Description*: All variable we need in a method have to be declared at the 
beginning of the method. If variable declared inside method body following 
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

*Title*: Using ```instanceof``` operator.

*Code:* **instance_of**

*Description*: Using of ```instanceof``` operator considered as pattern.

*Examples*: 

```java
public static void main(String[] args) {
    Child obj = new Child();
    if (obj instanceof String)
        System.out.println("obj is instance of Child");
}
```


***

*Title*: Force type casting.

*Code:* **force_type_cast**

*Description*: The force type casting considered as a pattern.

*Examples*:

```java
// casting to int is 
public int square (int n) {
    return (int) java.lang.Math.pow(n,2);
}
```

***

*Title*: String concatenation using ```+``` operator.

*Code:* **string_concat**

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

*Code:* **super_method_call**

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

*Title*: Line distance between variable declaration and first usage greater then threshold.

*Code:* **var_decl_diff**

*Description*: If line distance between variable declaration and first usage
exceeds some threshold we consider it as the pattern. We calculate only non-empty
lines.

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

*Title*: Class constructor except ```this``` contains other code.

*Code:* **smell_constructor**

*Description*: 

*Examples*:

***

*Title*: Usage of method chaining more than one time.

*Code*: **method_chain**

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

*Title*: Null checks

*Code*: **null_check**

*Description*: If we check that something equals null (except in constructor)
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

*Title*: Non final attributes

*Code*: **non_final_attribute**

*Description*: Once we see a mutable attribute (without final modifier), it's 
considered a pattern.

*Examples*:

```java
class Book {
  private int id;
  // something else
}
```
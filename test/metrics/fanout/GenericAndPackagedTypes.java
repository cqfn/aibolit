// Total FanOut = 2

import SomePackage;
import AnotherPackage.GenericType;

public class FirstClass {
    Map<SomePackage.SomeClass, GenericType<SomePackage.SomeClass>> field;       // +2 for SomeClass and GenericType
}

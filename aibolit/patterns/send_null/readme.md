Well known issues:

When passing a ternary operator with values containing "null" to some invocation, 
this is bot recognized as a pattern, but should be.

    doSomething(myString = ( ( myString != 5) ? null : myString ), obj)

The problem is: any expression with ternary operator send to invocation may have nested expressions inside. This problem requires more time to solve.

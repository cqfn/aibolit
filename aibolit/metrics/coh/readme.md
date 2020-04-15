### Cohesion with LCOM4
For `class A` with methods (functions: `func1`, `func2`, `func3`) and with attributes (`attr1`, `attr2`, `attr3`) we can build a graph `G1`:

![asd](https://github.com/silverCase/aibolit/blob/metrics/aibolit/metrics/coh/G1.png)

To measure the cohesion of class we will use `LCOM4` metric.\
To understand `LCOM4` take a look at `LCOM3`:\
`LCOM3` - calculates the number of connected component in the method graph. The methods in the graph are connected,
if methods have access to the same attribute.\
![aasd](https://github.com/silverCase/aibolit/blob/metrics/aibolit/metrics/coh/G2.png)

For graph `G1` metric `LCOM3 = 2`, because `func1` and `func2` have access to `attr2`.\
`LCOM4` differs from `LCOM3` with additional edges occuring when `func3` calls `func1`.\
For graph `G1` metric `LCOM4 = 1`


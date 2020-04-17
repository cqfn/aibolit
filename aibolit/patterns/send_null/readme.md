This pattern looks through full AST and finds all nodes containing `null` in attributes.
Also pattern works when a `TernaryExpression` with `null` value is passed to `Invocation`.
If you find any other possible scenarios – please make an issue.

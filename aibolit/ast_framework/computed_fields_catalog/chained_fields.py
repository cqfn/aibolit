# The MIT License (MIT)
#
# Copyright (c) 2020 Aibolit
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Union, Any, Callable
from itertools import chain

from aibolit.ast_framework import ASTNode


def chain_field_getter_factory(*steps: Union[str, int]) -> Callable[[ASTNode], Any]:
    """
    A chained field is a field of some other field and so on.
    For example name of class field is retrieved like `field_decl.declarators[0].name` using javalang fields.
    To automate this chain fields can be used.
    Chain field is specified by sequence of strings (field names) and integers (list indexes).
    If a field is list of ASTNodes and next step in chain is string
    then we get that field from every node in list.
    If we get list of lists, it gets flatten.
    List with single items is unwrapped.
    """

    def get_chain_field(node: ASTNode) -> Any:
        field = node
        for step in steps:
            if isinstance(field, list) and \
               isinstance(step, str) and \
               all(isinstance(item, ASTNode) for item in field):
                # get attribute from all elements from a list
                field = [getattr(item, step) for item in field]

                if all(isinstance(item, list) for item in field):  # flattening list
                    field = list(chain.from_iterable(field))

            elif isinstance(field, list) and isinstance(step, int):
                field = field[step]
            elif isinstance(field, ASTNode) and isinstance(step, str):
                field = getattr(field, step)
            else:
                raise RuntimeError(f"Failed to apply step {step} to field {field}.")

        if isinstance(field, list) and len(field) == 1:
            field = field[0]

        return field

    return get_chain_field

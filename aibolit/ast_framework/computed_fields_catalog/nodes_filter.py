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

from typing import Callable, Iterator

from aibolit.ast_framework import ASTNode, ASTNodeType


def nodes_filter_factory(
    base_field_name: str, *node_types: ASTNodeType
) -> Callable[[ASTNode], Iterator[ASTNode]]:
    """
    Create filter, which takes 'body_field_name' field of incoming node,
    checks if it list of ASTNode, and return it filtered by node_type.
    """

    def filter(base_node: ASTNode) -> Iterator[ASTNode]:
        base_field = getattr(base_node, base_field_name)
        if isinstance(base_field, list) and all(
            isinstance(item, ASTNode) for item in base_field
        ):
            for node in base_field:
                if node.node_type in node_types:
                    yield node
        else:
            raise RuntimeError(
                f"Failed computing ASTNode field based on {base_field_name} field. "
                f"Expected list, but got {base_field} of type {type(base_field)}."
            )

    return filter

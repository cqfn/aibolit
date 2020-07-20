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
from aibolit.ast_framework.computed_fields_registry import computed_fields_registry


def _create_filter(
    base_field_name: str, *node_types: ASTNodeType
) -> Callable[[ASTNode], Iterator[ASTNode]]:
    def filter(base_node: ASTNode) -> Iterator[ASTNode]:
        base_field = getattr(base_node, base_field_name)
        if not isinstance(base_field, list):
            raise RuntimeError(
                f"Failed computing ASTNode field based on {base_field_name} field. "
                f"Expected list, but got {base_field} of type {type(base_field)}."
            )
        for node in base_field:
            if isinstance(node, ASTNode) and node.node_type in node_types:
                yield node

    return filter


computed_fields_registry.register(
    _create_filter("body", ASTNodeType.CONSTRUCTOR_DECLARATION),
    "constructors",
    ASTNodeType.CLASS_DECLARATION,
    ASTNodeType.INTERFACE_DECLARATION,
    ASTNodeType.ANNOTATION_DECLARATION,
)


computed_fields_registry.register(
    _create_filter(
        "body", ASTNodeType.CONSTRUCTOR_DECLARATION, ASTNodeType.METHOD_DECLARATION
    ),
    "methods",
    ASTNodeType.CLASS_DECLARATION,
    ASTNodeType.INTERFACE_DECLARATION,
    ASTNodeType.ANNOTATION_DECLARATION,
)


computed_fields_registry.register(
    _create_filter("body", ASTNodeType.FIELD_DECLARATION),
    "fields",
    ASTNodeType.CLASS_DECLARATION,
    ASTNodeType.INTERFACE_DECLARATION,
    ASTNodeType.ANNOTATION_DECLARATION,
)


computed_fields_registry.register(
    _create_filter("declarations", ASTNodeType.METHOD_DECLARATION),
    "methods",
    ASTNodeType.CLASS_DECLARATION,
    ASTNodeType.INTERFACE_DECLARATION,
    ASTNodeType.ANNOTATION_DECLARATION,
)


computed_fields_registry.register(
    _create_filter("declarations", ASTNodeType.FIELD_DECLARATION),
    "fields",
    ASTNodeType.CLASS_DECLARATION,
    ASTNodeType.INTERFACE_DECLARATION,
    ASTNodeType.ANNOTATION_DECLARATION,
)

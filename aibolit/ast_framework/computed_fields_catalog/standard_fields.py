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

from aibolit.ast_framework.computed_fields_registry import computed_fields_registry
from aibolit.ast_framework import ASTNodeType

from .nodes_filter import nodes_filter_factory
from .chained_fields import chain_field_getter_factory


def register_standard_computed_properties() -> None:
    _register_standard_nodes_filters()
    _register_standard_chain_fields()


def _register_standard_nodes_filters() -> None:
    computed_fields_registry.register(
        nodes_filter_factory("body", ASTNodeType.CONSTRUCTOR_DECLARATION),
        "constructors",
        ASTNodeType.CLASS_DECLARATION,
        ASTNodeType.INTERFACE_DECLARATION,
        ASTNodeType.ANNOTATION_DECLARATION,
    )

    computed_fields_registry.register(
        nodes_filter_factory(
            "body", ASTNodeType.CONSTRUCTOR_DECLARATION, ASTNodeType.METHOD_DECLARATION
        ),
        "methods",
        ASTNodeType.CLASS_DECLARATION,
        ASTNodeType.INTERFACE_DECLARATION,
        ASTNodeType.ANNOTATION_DECLARATION,
    )

    computed_fields_registry.register(
        nodes_filter_factory("body", ASTNodeType.FIELD_DECLARATION),
        "fields",
        ASTNodeType.CLASS_DECLARATION,
        ASTNodeType.INTERFACE_DECLARATION,
        ASTNodeType.ANNOTATION_DECLARATION,
    )

    computed_fields_registry.register(
        nodes_filter_factory("declarations", ASTNodeType.METHOD_DECLARATION),
        "methods",
        ASTNodeType.ENUM_DECLARATION,
    )

    computed_fields_registry.register(
        nodes_filter_factory("declarations", ASTNodeType.FIELD_DECLARATION),
        "fields",
        ASTNodeType.ENUM_DECLARATION,
    )


def _register_standard_chain_fields() -> None:
    computed_fields_registry.register(
        chain_field_getter_factory("declarators", "name"),
        "name",
        ASTNodeType.CONSTANT_DECLARATION,
        ASTNodeType.FIELD_DECLARATION,
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ASTNodeType.VARIABLE_DECLARATION,
    )

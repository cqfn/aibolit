# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

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
        nodes_filter_factory("body", ASTNodeType.METHOD_DECLARATION),
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
        "names",
        ASTNodeType.CONSTANT_DECLARATION,
        ASTNodeType.FIELD_DECLARATION,
        ASTNodeType.LOCAL_VARIABLE_DECLARATION,
        ASTNodeType.VARIABLE_DECLARATION,
    )

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from enum import Enum
from typing import Any, Dict, Iterator, List, Set, Union

from networkx import (  # type: ignore
    DiGraph, strongly_connected_components, weakly_connected_components,
)

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.patterns.classic_setter.classic_setter import ClassicSetter as setter
from aibolit.patterns.classic_getter.classic_getter import ClassicGetter as getter


class DecompositionStrength(Enum):
    """
    Enum representing available decomposition strengths.
    """
    STRONG = "strong"
    WEAK = "weak"

    @classmethod
    def values(cls) -> List[str]::
        """
        Return available strength values.
        """
        return [item.value for item in cls]


def find_patterns(tree: AST, patterns: List[Any]) -> Set[str]:
    """
    Searches all setters in a component
    :param patterns: list of patterns to check
    :param tree: ast tree
    :return: list of method name which are setters
    """

    patterns_method_names: Set[str] = set()
    for method_declaration in tree.root().methods:
        method_ast = tree.subtree(method_declaration)
        for pattern in patterns:
            if is_ast_pattern(method_ast, pattern):
                patterns_method_names.add(method_declaration.name)

    return patterns_method_names


def is_ast_pattern(class_ast: AST, Pattern) -> bool:
    """
    Checks whether ast is some pattern
    :param Pattern: pattern class
    :param class_ast: ast tree
    :return: True if it is setter, otherwise - False
    """
    return len(Pattern().value(class_ast)) > 0


def decompose_java_class(
        class_ast: AST,
        sstrength: Union[DecompositionStrength, str] = DecompositionStrength.STRONG,
        ignore_setters=False,
        ignore_getters=False) -> List[AST]:
    """
    Splits java_class fields and methods by their usage and
    construct for each case an AST with only those fields and methods kept.
    :param class_ast: component
    :param ignore_getters: should ignore getters
    :param ignore_setters: should ignore setters
    :param strength: decomposition strength; accepts DecompositionStrength or 'strong'/'weak'
    for splitting fields and methods by strong and weak connectivity.
    """

    usage_graph = _create_usage_graph(class_ast)

    components: Iterator[Set[int]]
    if isinstance(strength, str):
        try:
            strength = DecompositionStrength(strength.lower())
        except ValueError:
            valid_strengths = [s.value for s in DecompositionStrength]
            raise ValueError(
                f'Unsupported decomposition strength: {strength}. '
                f'Must be one of: {valid_strengths}'
            )
    if strength == DecompositionStrength.STRONG:
        components = strongly_connected_components(usage_graph)
    elif strength == DecompositionStrength.WEAK:
        components = weakly_connected_components(usage_graph)
    else:
        valid_strengths = [s.value for s in DecompositionStrength]
        raise ValueError(f"Unsupported decomposition strength: {strength}. "
                         f"Must be one of: {valid_strengths}")

    class_parts: List[AST] = []
    patterns_to_ignore: List[Any] = []
    if ignore_getters:
        patterns_to_ignore.append(getter)
    if ignore_setters:
        patterns_to_ignore.append(setter)

    if ignore_setters or ignore_getters:
        prohibited_function_names = find_patterns(class_ast, patterns_to_ignore)

    for component in components:

        field_names = {
            usage_graph.nodes[node]['name']
            for node in component
            if usage_graph.nodes[node]['type'] == 'field'
        }
        method_names = {
            usage_graph.nodes[node]['name']
            for node in component
            if usage_graph.nodes[node]['type'] == 'method'
        }

        if ignore_setters or ignore_getters:
            method_names = method_names.difference(prohibited_function_names)

        filtered = class_ast.with_fields_and_methods(field_names, method_names)

        class_parts.append(
            filtered
        )

    return class_parts


def _create_usage_graph(class_ast: AST) -> DiGraph:
    usage_graph = DiGraph()
    fields_ids: Dict[str, int] = {}
    methods_ids: Dict[str, int] = {}

    class_declaration = class_ast.root()

    for field_declaration in class_declaration.fields:
        # several fields can be declared at one line
        for field_name in field_declaration.names:
            fields_ids[field_name] = len(fields_ids)
            usage_graph.add_node(fields_ids[field_name], type='field', name=field_name)

    for method_declaration in class_declaration.methods:
        method_name = method_declaration.name

        # overloaded methods considered as single node in usage_graph
        if method_name not in methods_ids:
            methods_ids[method_name] = len(fields_ids) + 1 + len(methods_ids)
            usage_graph.add_node(
                methods_ids[method_name], type='method', name=method_name
            )

    for method_declaration in class_declaration.methods:
        method_ast = class_ast.subtree(method_declaration)

        for invoked_method_name in _find_local_method_invocations(method_ast):
            if invoked_method_name in methods_ids:
                usage_graph.add_edge(
                    methods_ids[method_declaration.name],
                    methods_ids[invoked_method_name],
                )

        for used_field_name in _find_fields_usage(method_ast):
            if used_field_name in fields_ids:
                usage_graph.add_edge(
                    methods_ids[method_declaration.name], fields_ids[used_field_name]
                )

    return usage_graph


def _find_local_method_invocations(method_ast: AST) -> Set[str]:
    invoked_methods: Set[str] = set()
    for method_invocation in method_ast.proxy_nodes(ASTNodeType.METHOD_INVOCATION):
        if method_invocation.qualifier is None:
            invoked_methods.add(method_invocation.member)

    return invoked_methods


def _find_fields_usage(method_ast: AST) -> Set[str]:
    local_variables: Set[str] = set()
    for variable_declaration in method_ast.proxy_nodes(
            ASTNodeType.LOCAL_VARIABLE_DECLARATION
    ):
        local_variables.update(variable_declaration.names)

    method_declaration = method_ast.root()
    for parameter in method_declaration.parameters:
        local_variables.add(parameter.name)

    used_fields: Set[str] = set()
    for member_reference in method_ast.proxy_nodes(ASTNodeType.MEMBER_REFERENCE):
        if member_reference.qualifier is None and \
                member_reference.member not in local_variables:
            used_fields.add(member_reference.member)

    return used_fields

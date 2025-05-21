# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import List, Dict, Set, Iterator, Any

from networkx import (  # type: ignore
    DiGraph, strongly_connected_components, weakly_connected_components
)

from aibolit.ast_framework import AST, ASTNodeType

from aibolit.patterns.classic_setter.classic_setter import ClassicSetter as setter
from aibolit.patterns.classic_getter.classic_getter import ClassicGetter as getter


def find_patterns(tree: AST, patterns: List[Any]) -> Set[str]:
    """
    Searches all setters in a component
    :param patterns: list of patterns to check
    :param tree: ast tree
    :return: list of method name which are setters
    """

    patterns_method_names: Set[str] = set()
    for method_declaration in tree.get_root().methods:
        method_ast = tree.get_subtree(method_declaration)
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
        strength: str,
        ignore_setters=False,
        ignore_getters=False) -> List[AST]:
    """
    Splits java_class fields and methods by their usage and
    construct for each case an AST with only those fields and methods kept.
    :param class_ast: component
    :param ignore_getters: should ignore getters
    :param ignore_setters: should ignore setters
    :param strength: controls splitting criteria. Use "strong" or "weak"
    for splitting fields and methods by strong and weak connectivity.
    """

    usage_graph = _create_usage_graph(class_ast)

    components: Iterator[Set[int]]
    if strength == "strong":
        components = strongly_connected_components(usage_graph)
    elif strength == "weak":
        components = weakly_connected_components(usage_graph)
    else:
        raise ValueError(
            f"'strength' argument must be either 'strong' or 'weak', but '{strength}' was provided."
        )

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
            usage_graph.nodes[node]["name"]
            for node in component
            if usage_graph.nodes[node]["type"] == "field"
        }
        method_names = {
            usage_graph.nodes[node]["name"]
            for node in component
            if usage_graph.nodes[node]["type"] == "method"
        }

        if ignore_setters or ignore_getters:
            method_names = method_names.difference(prohibited_function_names)

        filtered = _filter_class_methods_and_fields(class_ast, field_names, method_names)

        class_parts.append(
            filtered
        )

    return class_parts


def _create_usage_graph(class_ast: AST) -> DiGraph:
    usage_graph = DiGraph()
    fields_ids: Dict[str, int] = {}
    methods_ids: Dict[str, int] = {}

    class_declaration = class_ast.get_root()

    for field_declaration in class_declaration.fields:
        # several fields can be declared at one line
        for field_name in field_declaration.names:
            fields_ids[field_name] = len(fields_ids)
            usage_graph.add_node(fields_ids[field_name], type="field", name=field_name)

    for method_declaration in class_declaration.methods:
        method_name = method_declaration.name

        # overloaded methods considered as single node in usage_graph
        if method_name not in methods_ids:
            methods_ids[method_name] = len(fields_ids) + 1 + len(methods_ids)
            usage_graph.add_node(
                methods_ids[method_name], type="method", name=method_name
            )

    for method_declaration in class_declaration.methods:
        method_ast = class_ast.get_subtree(method_declaration)

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
    for method_invocation in method_ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION):
        if method_invocation.qualifier is None:
            invoked_methods.add(method_invocation.member)

    return invoked_methods


def _find_fields_usage(method_ast: AST) -> Set[str]:
    local_variables: Set[str] = set()
    for variable_declaration in method_ast.get_proxy_nodes(
            ASTNodeType.LOCAL_VARIABLE_DECLARATION
    ):
        local_variables.update(variable_declaration.names)

    method_declaration = method_ast.get_root()
    for parameter in method_declaration.parameters:
        local_variables.add(parameter.name)

    used_fields: Set[str] = set()
    for member_reference in method_ast.get_proxy_nodes(ASTNodeType.MEMBER_REFERENCE):
        if member_reference.qualifier is None and \
                member_reference.member not in local_variables:
            used_fields.add(member_reference.member)

    return used_fields


def _filter_class_methods_and_fields(
        class_ast: AST,
        allowed_fields_names: Set[str],
        allowed_methods_names: Set[str]
) -> AST:
    class_declaration = class_ast.get_root()
    allowed_nodes = {class_declaration.node_index}

    for field_declaration in class_declaration.fields:
        if len(allowed_fields_names & set(field_declaration.names)) != 0:
            field_ast = class_ast.get_subtree(field_declaration)
            allowed_nodes.update(node.node_index for node in field_ast)

    for method_declaration in class_declaration.methods:
        if method_declaration.name in allowed_methods_names:
            method_ast = class_ast.get_subtree(method_declaration)
            allowed_nodes.update(node.node_index for node in method_ast)

    return AST(class_ast.tree.subgraph(allowed_nodes), class_declaration.node_index)

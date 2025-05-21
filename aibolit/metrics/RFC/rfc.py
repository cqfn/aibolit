# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import Set, NamedTuple

from aibolit.ast_framework import AST, ASTNode, ASTNodeType


class _MethodInvocationParams(NamedTuple):
    isLocal: bool
    name: str


class RFC:
    """
    The Response For a Class (RFC) is an object-oriented metric
    that shows the interaction of the class methods with other methods.
    This implementation accept arbitrary AST and
    return sum of RFC for all class declaration in it.
    To calculate RFC of a class we count number of public methods and
    number of distinct methods invocation in those methods.
    """

    def value(self, ast: AST) -> int:
        rfc = 0
        for class_declaration in ast.get_proxy_nodes(ASTNodeType.CLASS_DECLARATION):
            rfc += self._calculate_class_RFC(ast.get_subtree(class_declaration))

        return rfc

    def _calculate_class_RFC(self, java_class: AST) -> int:
        class_declaration = java_class.get_root()
        assert class_declaration.node_type == ASTNodeType.CLASS_DECLARATION

        rfc = 0
        invoked_methods: Set[_MethodInvocationParams] = set()
        local_methods_names: Set[str] = set()
        for method_ast in java_class.get_subtrees(ASTNodeType.METHOD_DECLARATION):
            method_declaration = method_ast.get_root()
            local_methods_names.add(method_declaration.name)
            if "public" in method_declaration.modifiers:
                rfc += 1
                invoked_methods |= self._get_all_method_invocation_params(method_ast)

        # filter out inherited methods
        # consider local methods with name not found
        # among methods names of current class as inherited
        invoked_methods = {
            invoked_method
            for invoked_method in invoked_methods
            if not invoked_method.isLocal or invoked_method.name in local_methods_names
        }

        rfc += len(invoked_methods)
        return rfc

    def _get_all_method_invocation_params(self, ast: AST) -> Set[_MethodInvocationParams]:
        return {
            self._create_method_invocation_params(method_invocation)
            for method_invocation in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION)
        }

    def _create_method_invocation_params(self,
                                         method_invocation: ASTNode) -> _MethodInvocationParams:
        assert method_invocation.node_type == ASTNodeType.METHOD_INVOCATION
        return _MethodInvocationParams(
            isLocal=method_invocation.qualifier is None, name=method_invocation.member
        )

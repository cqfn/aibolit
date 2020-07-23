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
        for class_item in class_declaration.body:
            if class_item.node_type == ASTNodeType.METHOD_DECLARATION:
                local_methods_names.add(class_item.name)
                if "public" in class_item.modifiers:
                    rfc += 1
                    invoked_methods |= self._get_all_method_invocation_params(
                        java_class.get_subtree(class_item)
                    )

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

    def _get_all_method_invocation_params(
        self, ast: AST
    ) -> Set[_MethodInvocationParams]:
        return {
            self._create_method_invocation_params(method_invocation)
            for method_invocation in ast.get_proxy_nodes(ASTNodeType.METHOD_INVOCATION)
        }

    def _create_method_invocation_params(
        self, method_invocation: ASTNode
    ) -> _MethodInvocationParams:
        assert method_invocation.node_type == ASTNodeType.METHOD_INVOCATION
        return _MethodInvocationParams(
            isLocal=len(method_invocation.qualifier) == 0, name=method_invocation.member
        )

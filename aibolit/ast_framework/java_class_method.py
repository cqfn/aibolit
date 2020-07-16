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

from cached_property import cached_property  # type: ignore
from typing import Dict, Set, TYPE_CHECKING
from networkx import DiGraph, dfs_tree  # type: ignore
from deprecated import deprecated  # type: ignore

from aibolit.utils.cfg_builder import build_cfg
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class_field import JavaClassField

if TYPE_CHECKING:
    from aibolit.ast_framework.java_class import JavaClass


@deprecated("This functionality must be transmitted to ASTNode")
class JavaClassMethod(AST):
    def __init__(self, tree: DiGraph, root: int, java_class: 'JavaClass'):
        self.tree = tree
        self.root = root
        self._java_class = java_class

    @cached_property
    def name(self) -> str:
        try:
            method_name = next(self.children_with_type(self.root, ASTNodeType.STRING))
            return self.tree.nodes[method_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def java_class(self) -> 'JavaClass':
        return self._java_class

    @cached_property
    def parameters(self) -> Dict[str, AST]:
        parameters: Dict[str, AST] = {}
        for parameter_node in self.children_with_type(self.root, ASTNodeType.FORMAL_PARAMETER):
            parameter_name_node = next(iter(self.children_with_type(parameter_node, ASTNodeType.STRING)))
            parameter_name = self.get_attr(parameter_name_node, 'string')
            parameters[parameter_name] = AST(dfs_tree(self.tree, parameter_node), parameter_node)

        return parameters

    @cached_property
    def used_methods(self) -> Dict[str, Set['JavaClassMethod']]:
        method_invocation_nodes = self.get_nodes(ASTNodeType.METHOD_INVOCATION)
        used_method_invocation_params = (self.get_method_invocation_params(node) for node
                                         in method_invocation_nodes)
        used_local_method_invocation_params = (params for params in used_method_invocation_params
                                               if len(params.object_name) == 0)
        used_local_method_names = {params.method_name for params in used_local_method_invocation_params}

        return {method_name: self.java_class.methods[method_name] for method_name in self.java_class.methods
                if method_name in used_local_method_names}

    @cached_property
    def used_fields(self) -> Dict[str, JavaClassField]:
        used_member_reference_params = (self.get_member_reference_params(node) for node in
                                        self.get_nodes(ASTNodeType.MEMBER_REFERENCE))
        used_local_member_reference_names = {params.member_name for params in used_member_reference_params
                                             if params.object_name == ''}
        # Local member references may lead to method parameters instead of class fields if they have same names
        used_local_member_reference_names -= self.parameters.keys()
        class_fields = self.java_class.fields
        return {field_name: class_fields[field_name] for field_name in used_local_member_reference_names}

    @cached_property
    def cfg(self) -> DiGraph:
        '''Make Control Flow Graph representation of this method'''
        return build_cfg(self)

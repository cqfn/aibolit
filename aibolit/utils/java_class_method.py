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
from networkx import DiGraph  # type: ignore
from aibolit.utils.cfg_builder import build_cfg

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_class_field import JavaClassField

if TYPE_CHECKING:
    from aibolit.utils.java_class import JavaClass


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
    def used_methods(self) -> Dict[str, Set['JavaClassMethod']]:
        method_invocation_nodes = self.nodes_by_type(ASTNodeType.METHOD_INVOCATION)
        used_method_invocation_params = (self.get_method_invoked_name(node) for node in method_invocation_nodes)
        used_local_method_invocation_params = (params for params in used_method_invocation_params
                                               if len(params.object_name) == 0)
        used_local_method_names = {params.method_name for params in used_local_method_invocation_params}

        return {method_name: self.java_class.methods[method_name] for method_name in self.java_class.methods
                if method_name in used_local_method_names}

    @cached_property
    def used_fields(self) -> Dict[str, Set[JavaClassField]]:
        pass

    @cached_property
    def cfg(self) -> DiGraph:
        '''Make Control Flow Graph representation of this method'''
        return build_cfg(self)

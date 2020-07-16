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
from deprecated import deprecated  # type: ignore

from typing import TYPE_CHECKING
from networkx import DiGraph  # type: ignore

from aibolit.ast_framework import AST, ASTNodeType

if TYPE_CHECKING:
    from aibolit.ast_framework.java_class import JavaClass


@deprecated("This functionality must be transmitted to ASTNode")
class JavaClassField(AST):
    def __init__(self, tree: DiGraph, root: int, java_class: 'JavaClass'):
        self.tree = tree
        self.root = root
        self._java_class = java_class

    @cached_property
    def name(self) -> str:
        try:
            field_declarator = next(self.children_with_type(self.root, ASTNodeType.VARIABLE_DECLARATOR))
            field_name = next(self.children_with_type(field_declarator, ASTNodeType.STRING))
            return self.tree.nodes[field_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def java_class(self) -> 'JavaClass':
        return self._java_class

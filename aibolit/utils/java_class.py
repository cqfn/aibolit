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


from functools import lru_cache

from typing import Iterator, TYPE_CHECKING
from networkx import DiGraph  # type: ignore

from aibolit.utils.ast import AST, ASTNodeType
from aibolit.utils.java_class_method import JavaClassMethod
from aibolit.utils.java_class_field import JavaClassField

if TYPE_CHECKING:
    from aibolit.utils.java_package import JavaPackage


class JavaClass(AST):
    def __init__(self, tree: DiGraph, root: int, java_package: 'JavaPackage'):
        self.tree = tree
        self.root = root
        self._java_package = java_package

    @property  # type: ignore
    @lru_cache
    def name(self) -> str:
        try:
            class_name = next(self.children_with_type(self.root, ASTNodeType.STRING))
            return self.tree.nodes[class_name]['string']
        except StopIteration:
            raise ValueError("Provided AST does not has 'STRING' node type right under the root")

    @property
    def package(self) -> 'JavaPackage':
        return self._java_package

    @property  # type: ignore
    @lru_cache
    def methods(self) -> Iterator[JavaClassMethod]:
        for nodes in self.subtrees_with_root_type(ASTNodeType.METHOD_DECLARATION):
            yield JavaClassMethod(self.tree.subgraph(nodes), nodes[0], self)

    @property  # type: ignore
    @lru_cache
    def fields(self) -> Iterator[JavaClassField]:
        for nodes in self.subtrees_with_root_type(ASTNodeType.FIELD_DECLARATION):
            yield JavaClassField(self.tree.subgraph(nodes), nodes[0], self)

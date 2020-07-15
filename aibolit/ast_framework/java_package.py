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

from typing import Dict

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.java_class import JavaClass


@deprecated("This functionality must be transmitted to ASTNode")
class JavaPackage(AST):
    def __init__(self, filename: str):
        ast = AST.build_from_javalang(build_ast(filename))
        super().__init__(ast.tree, ast.root)

    @cached_property
    def name(self) -> str:
        try:
            package_declaration = next(self.children_with_type(self.root, ASTNodeType.PACKAGE_DECLARATION))
            package_name = next(self.children_with_type(package_declaration, ASTNodeType.STRING))
            return self.tree.nodes[package_name]['string']
        except StopIteration:
            pass

        return '.'  # default package name

    @cached_property
    def java_classes(self) -> Dict[str, JavaClass]:
        classes: Dict[str, JavaClass] = {}
        for class_ast in self.get_subtrees(ASTNodeType.CLASS_DECLARATION):
            java_class = JavaClass(class_ast.tree, class_ast.root, self)
            classes[java_class.name] = java_class
        return classes

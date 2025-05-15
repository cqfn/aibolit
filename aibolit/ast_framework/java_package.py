# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from typing import Dict

from cached_property import cached_property  # type: ignore
from deprecated import deprecated  # type: ignore

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
            package_declaration = next(
                self.children_with_type(self.root, ASTNodeType.PACKAGE_DECLARATION)
            )
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

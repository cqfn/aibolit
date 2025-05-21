# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase, skip
from pathlib import Path

from aibolit.ast_framework.java_package import JavaPackage
from aibolit.ast_framework import ASTNodeType


@skip('JavaClass is deprecated')
class JavaClassTestCase(TestCase):
    def test_class_name(self):
        for filename, class_names in JavaClassTestCase._java_packages_with_class_names:
            with self.subTest(f'Filename: {filename}'):
                java_package = JavaPackage(Path(__file__).parent.absolute() / filename)
                self.assertEqual(java_package.java_classes.keys(), class_names)

    def test_class_method(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'SimpleClass.java')
        java_class = java_package.java_classes['Simple']
        java_methods = java_class.methods['Increment']
        self.assertEqual(len(java_methods), 1)
        java_method = next(iter(java_methods))
        java_method_node_types = [java_method.get_type(node) for node in java_method.get_nodes()]
        self.assertEqual(
            java_method_node_types, JavaClassTestCase._java_method_preorder_traversal_types
        )

    def test_class_field(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / 'SimpleClass.java')
        java_class = java_package.java_classes['Simple']
        java_field = java_class.fields['x']
        java_field_node_types = [java_field.get_type(node) for node in java_field.get_nodes()]
        self.assertEqual(
            java_field_node_types, JavaClassTestCase._java_field_preorder_traversal_types
        )

    _java_packages_with_class_names = [
        ('SimpleClass.java', {'Simple'}),
        ('TwoClasses.java', {'First', 'Second'})
    ]

    _java_method_preorder_traversal_types = [
        ASTNodeType.METHOD_DECLARATION,
        ASTNodeType.COLLECTION,
        ASTNodeType.STRING,
        ASTNodeType.BASIC_TYPE,
        ASTNodeType.STRING,
        ASTNodeType.STRING,
        ASTNodeType.STATEMENT_EXPRESSION,
        ASTNodeType.ASSIGNMENT,
        ASTNodeType.MEMBER_REFERENCE,
        ASTNodeType.STRING,
        ASTNodeType.STRING,
        ASTNodeType.LITERAL,
        ASTNodeType.STRING,
        ASTNodeType.STRING,
        ASTNodeType.RETURN_STATEMENT,
        ASTNodeType.MEMBER_REFERENCE,
        ASTNodeType.STRING,
        ASTNodeType.STRING,
    ]

    _java_field_preorder_traversal_types = [
        ASTNodeType.FIELD_DECLARATION,
        ASTNodeType.COLLECTION,
        ASTNodeType.STRING,
        ASTNodeType.BASIC_TYPE,
        ASTNodeType.STRING,
        ASTNodeType.VARIABLE_DECLARATOR,
        ASTNodeType.STRING,
        ASTNodeType.LITERAL,
        ASTNodeType.STRING,
    ]

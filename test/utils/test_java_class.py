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

from unittest import TestCase
from pathlib import Path

from aibolit.utils.java_package import JavaPackage
from aibolit.utils.ast import ASTNodeType


class JavaClassTestCase(TestCase):
    def test_class_name(self):
        for filename, class_names in JavaClassTestCase._java_packages_with_class_names:
            with self.subTest():
                java_package = JavaPackage(Path(__file__).parent.absolute() / filename)
                for java_class, class_name in zip(java_package.java_classes, class_names):
                    self.assertEqual(java_class.name, class_name)

    def test_class_mathod(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / "SimpleClass.java")
        java_class = next(java_package.java_classes)
        java_method = next(java_class.methods)
        self.assertEqual(list(java_method.node_types), JavaClassTestCase._java_method_preorder_traversal_types)

    def test_class_field(self):
        java_package = JavaPackage(Path(__file__).parent.absolute() / "SimpleClass.java")
        java_class = next(java_package.java_classes)
        java_method = next(java_class.fields)
        self.assertEqual(list(java_method.node_types), JavaClassTestCase._java_field_preorder_traversal_types)

    _java_packages_with_class_names = [
        ("SimpleClass.java", ["Simple"]),
        ("TwoClasses.java", ["First", "Second"])
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

# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path

from aibolit.metrics.RFC.rfc import RFC
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class RFCTestSuite(TestCase):
    def test_empty_public_methods(self):
        ast = RFCTestSuite._get_ast("EmptyPublicMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 2)

    def test_empty_public_and_private_methods(self):
        ast = RFCTestSuite._get_ast("EmptyPublicAndPrivateMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 2)

    def test_public_methods_invoke_public_methods(self):
        ast = RFCTestSuite._get_ast("PublicMethodsInvokePublicMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 3)

    def test_public_methods_invoke_private_methods(self):
        ast = RFCTestSuite._get_ast("PublicMethodsInvokePrivateMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 3)

    def test_public_methods_invoke_outer_methods(self):
        ast = RFCTestSuite._get_ast("PublicMethodsInvokeOuterMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 3)

    def test_several_invocation_of_same_method(self):
        ast = RFCTestSuite._get_ast("SeveralInvocationOfSameMethod.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 4)

    def test_invocation_of_local_and_outer_methods_with_same_name(self):
        ast = RFCTestSuite._get_ast("InvocationOfLocalAndOuterMethodsWithSameName.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 4)

    def test_several_classes(self):
        ast = RFCTestSuite._get_ast("SeveralClasses.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 2)

    def test_inherited_methods(self):
        ast = RFCTestSuite._get_ast("InheritedMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 2)

    def test_overwritten_inherited_methods(self):
        ast = RFCTestSuite._get_ast("OverwrittenInheritedMethods.java")
        rfc = RFC()
        self.assertEqual(rfc.value(ast), 2)

    @staticmethod
    def _get_ast(filename: str) -> AST:
        path = Path(__file__).absolute().parent / filename
        return AST.build_from_javalang(build_ast(str(path)))

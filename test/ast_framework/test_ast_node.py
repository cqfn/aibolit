# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class ASTNodeTestSuite(TestCase):
    def test_class_computed_fields(self):
        ast = AST.build_from_javalang(
            build_ast(
                Path(__file__).absolute().parent / "MethodUseOtherMethodExample.java"
            )
        )
        package = ast.get_root()
        assert len(package.types) == 1 and \
            package.types[0].node_type == ASTNodeType.CLASS_DECLARATION

        java_class = package.types[0]
        self.assertEqual(java_class.name, "MethodUseOtherMethod")
        self.assertEqual(java_class.modifiers, set())
        self.assertEqual(java_class.documentation, "/**\n* Some documentation\n*/")

        # consider each field declaration declares single field
        fields_names = {field.names[0] for field in java_class.fields}
        self.assertEqual(fields_names, {"connectingField", "redundantField"})

        methods_names = {method.name for method in java_class.methods}
        self.assertEqual(
            methods_names,
            {
                "useOnlyMethods1",
                "useOnlyMethods2",
                "getField",
                "setField",
                "standAloneMethod",
                "shadowing",
            },
        )

        self.assertEqual(set(java_class.constructors), set())

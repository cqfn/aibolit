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

from aibolit.ast_framework import AST, ASTNodeType
from aibolit.utils.ast_builder import build_ast


class ASTNodeTestSuite(TestCase):
    def test_fields(self):
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

        fields_names = {field.name for field in java_class.fields}
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

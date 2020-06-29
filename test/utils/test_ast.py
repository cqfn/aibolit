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
from itertools import zip_longest

from aibolit.utils.ast_builder import build_ast
from aibolit.utils.ast import AST, ASTNodeType, MemberReferenceParams, MethodInvocationParams


class ASTTestSuite(TestCase):
    def test_parsing(self):
        ast = self._build_ast("SimpleClass.java")
        self.assertEqual(list(ast.node_types),
                         ASTTestSuite._java_simple_class_preordered)

    def test_subtrees_selection(self):
        ast = self._build_ast("SimpleClass.java")
        subtrees = ast.subtrees_with_root_type(ASTNodeType.BASIC_TYPE)
        for subtree_nodes, expected_subtree in \
                zip_longest(subtrees, ASTTestSuite._java_simple_class_basic_type_subtrees):
            with self.subTest():
                self.assertEqual(subtree_nodes, expected_subtree)

    def test_member_reference_params(self):
        ast = self._build_ast("MemberReferencesExample.java")
        for node, expected_params in zip_longest(ast.nodes_by_type(ASTNodeType.MEMBER_REFERENCE),
                                                 ASTTestSuite._expected_member_reference_params):
            self.assertEqual(ast.get_member_reference_params(node), expected_params)

    def test_method_invocation_params(self):
        ast = self._build_ast("MethodInvokeExample.java")
        for node, expected_params in zip_longest(ast.nodes_by_type(ASTNodeType.METHOD_INVOCATION),
                                                 ASTTestSuite._expected_method_invocation_params):
            self.assertEqual(ast.get_method_invocation_params(node), expected_params)

    def _build_ast(self, filename: str):
        javalang_ast = build_ast(Path(__file__).parent.absolute() / filename)
        return AST.build_from_javalang(javalang_ast)

    _java_simple_class_preordered = [
        ASTNodeType.COMPILATION_UNIT,
        ASTNodeType.CLASS_DECLARATION,
        ASTNodeType.COLLECTION,
        ASTNodeType.STRING,
        ASTNodeType.FIELD_DECLARATION,
        ASTNodeType.COLLECTION,
        ASTNodeType.STRING,
        ASTNodeType.BASIC_TYPE,
        ASTNodeType.STRING,
        ASTNodeType.VARIABLE_DECLARATOR,
        ASTNodeType.STRING,
        ASTNodeType.LITERAL,
        ASTNodeType.STRING,
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

    _java_simple_class_basic_type_subtrees = [
        [8, 9],
        [17, 18],
    ]

    _expected_member_reference_params = [
        MemberReferenceParams('', 'block_variable', ''),
        MemberReferenceParams('', 'method_parameter', ''),
        MemberReferenceParams('', 'block_variable', '++'),
        MemberReferenceParams('', 'field', ''),
        MemberReferenceParams('', 'block_variable', ''),
        MemberReferenceParams('Something', 'outer_field', ''),
        MemberReferenceParams('', 'field', ''),
    ]

    _expected_method_invocation_params = [
        MethodInvocationParams(object_name='System.out', method_name='println'),
        MethodInvocationParams(object_name='', method_name='method1'),
    ]

# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path
from itertools import zip_longest

from aibolit.utils.ast_builder import build_ast
from aibolit.ast_framework import AST, ASTNodeType
from aibolit.ast_framework.ast import MemberReferenceParams, MethodInvocationParams


class ASTTestSuite(TestCase):
    def test_parsing(self):
        ast = self._build_ast('SimpleClass.java')
        actual_node_types = [node.node_type for node in ast]
        self.assertEqual(actual_node_types,
                         ASTTestSuite._java_simple_class_preordered)

    def test_subtrees_selection(self):
        ast = self._build_ast('SimpleClass.java')
        subtrees = ast.subtrees(ASTNodeType.BASIC_TYPE)
        for actual_subtree, expected_subtree in \
                zip_longest(subtrees, ASTTestSuite._java_simple_class_basic_type_subtrees):
            with self.subTest():
                self.assertEqual([node.node_index for node in actual_subtree],
                                 expected_subtree)

    def test_complex_fields(self):
        ast = self._build_ast('StaticConstructor.java')
        class_declaration = next((declaration for declaration in ast.root().types if
                                 declaration.node_type == ASTNodeType.CLASS_DECLARATION), None)
        assert class_declaration is not None, 'Cannot find class declaration'

        static_constructor, method_declaration = class_declaration.body
        self.assertEqual([node.node_type for node in static_constructor],
                         [ASTNodeType.STATEMENT_EXPRESSION, ASTNodeType.STATEMENT_EXPRESSION])
        self.assertEqual(method_declaration.node_type, ASTNodeType.METHOD_DECLARATION)

    def test_with_fields_and_methods_empty(self):
        ast = next(self._build_ast('SimpleClass.java').subtrees(ASTNodeType.CLASS_DECLARATION))
        nothing_ast = ast.with_fields_and_methods(set(), set())
        self.assertEqual(self._field_names(nothing_ast), [])
        self.assertEqual(self._method_names(nothing_ast), [])

    def test_with_fields_and_methods_only_methods(self):
        ast = next(self._build_ast('SimpleClass.java').subtrees(ASTNodeType.CLASS_DECLARATION))
        method_ast = ast.with_fields_and_methods(set(), {'Increment'})
        self.assertEqual(self._field_names(method_ast), [])
        self.assertEqual(self._method_names(method_ast), ['Increment'])

    def test_with_fields_and_methods_only_fields(self):
        ast = next(self._build_ast('SimpleClass.java').subtrees(ASTNodeType.CLASS_DECLARATION))
        field_ast = ast.with_fields_and_methods({'x'}, set())
        self.assertEqual(self._field_names(field_ast), ['x'])
        self.assertEqual(self._method_names(field_ast), [])

    def test_with_fields_and_methods(self):
        ast = next(self._build_ast('SimpleClass.java').subtrees(ASTNodeType.CLASS_DECLARATION))
        method_field_ast = ast.with_fields_and_methods({'x'}, {'Increment'})
        self.assertEqual(self._field_names(method_field_ast), ['x'])
        self.assertEqual(self._method_names(method_field_ast), ['Increment'])

    def _build_ast(self, filename: str):
        javalang_ast = build_ast(str(Path(__file__).parent.absolute() / filename))
        return AST.build_from_javalang(javalang_ast)

    def _field_names(self, ast: AST) -> list[str]:
        result = set()
        for field_declaration in ast.proxy_nodes(ASTNodeType.FIELD_DECLARATION):
            for name in field_declaration.names:
                result.add(name)
        return sorted(result)

    def _method_names(self, ast: AST) -> list[str]:
        result = set()
        for method_declaration in ast.proxy_nodes(ASTNodeType.METHOD_DECLARATION):
            result.add(method_declaration.name)
        return sorted(result)

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

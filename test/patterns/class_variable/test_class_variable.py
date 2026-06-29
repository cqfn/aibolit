# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.patterns.class_variable.class_variable import ClassVariable
from aibolit.utils.ast_builder import build_ast


class ClassVariableTestCase(TestCase):
    @staticmethod
    def _find_lines(source_code: str):
        with TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir, 'Book.java')
            filepath.write_text(dedent(source_code), encoding='utf-8')
            ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassVariable()
        return pattern.value(ast)

    def test_find_class_variable(self):
        lines = self._find_lines(
            '''\
            import java.util.ArrayList;

            class Book {
                void foo() {
                    ArrayList<Integer> list = new ArrayList<>();
                }
            }
            '''
        )
        self.assertEqual(lines, [5])

    def test_ignore_interface_variable(self):
        lines = self._find_lines(
            '''\
            import java.util.ArrayList;
            import java.util.List;

            class Book {
                void foo() {
                    List<Integer> list = new ArrayList<>();
                }
            }
            '''
        )
        self.assertEqual(lines, [])

    def test_ignore_primitive_variable(self):
        lines = self._find_lines(
            '''\
            class Book {
                void foo() {
                    int number = 42;
                }
            }
            '''
        )
        self.assertEqual(lines, [])

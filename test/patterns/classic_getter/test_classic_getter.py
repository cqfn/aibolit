# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from textwrap import dedent
from unittest import TestCase

from aibolit.patterns.classic_getter.classic_getter import ClassicGetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class ClassicGetterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_no_getters(self):
        filepath = self.current_directory / 'NoGetters.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_fake_getter(self):
        filepath = self.current_directory / 'FakeGetter.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_long_fake_getter(self):
        filepath = self.current_directory / 'LongFake.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple(self):
        filepath = self.current_directory / 'SimpleGetter.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicGetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8])


def test_getter_using_this_reference() -> None:
    content = dedent(
        '''\
        class Dummy {
            private int value;
            public int getValue() {
                return this.value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_getSomething_method_that_does_not_return() -> None:
    content = dedent(
        '''\
        class Dummy {
            public void getProudOfThisCode() {
                System.out.println('This code does not have getters');
            }
        }
        '''
    ).strip()
    assert not _offending_lines(content)


def _offending_lines(content: str) -> list[int]:
    """Return a list of lines offending ClassicGetter pattern."""
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = ClassicGetter()
    return pattern.value(ast)

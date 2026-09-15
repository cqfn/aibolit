# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent

from aibolit.patterns.er_class.er_class import ErClass
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast_from_string


def test_manager_in_middle() -> None:
    content = dedent(
        '''\
        class AnimatableManagerSplit {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_controller_in_end() -> None:
    content = dedent(
        '''\
        class FooController {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_one_normal_class() -> None:
    content = dedent(
        '''\
        class Dummy {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_two_classes_with_pattern() -> None:
    content = dedent(
        '''\
        abstract class BaseKeyframeAnimationManager {
        }

        class EmptyKeyframeWrapperListener {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1, 4]


def test_class_parser() -> None:
    content = dedent(
        '''\
        class Configuration {
            private class Parser {
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [2]


def test_another_normal_class() -> None:
    content = dedent(
        '''\
        class FillContent {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_four_normal_classes() -> None:
    content = dedent(
        '''\
        class One {}
        class Two {}
        class Three {}
        class Four {}
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_two_distant_normal_classes() -> None:
    content = dedent(
        '''\
        class FirstNormal {
        }

        class SecondNormal {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_classes_in_comments() -> None:
    content = dedent(
        '''\
        class Dummy {
            // class FooManager should not match
            /* class BarController */
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_classes_in_methods() -> None:
    content = dedent(
        '''\
        class Dummy {
            void run() {
                String manager = "controller";
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_normal_class() -> None:
    content = dedent(
        '''\
        class RectangleContent {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_three_writers_one_reader() -> None:
    content = dedent(
        '''\
        class SequenceFile {
            public static class Writer {
            }
            static class RecordCompressWriter extends Writer {
            }
            static class BlockCompressWriter extends Writer {
            }
            public static class Reader {
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [2, 4, 6, 8]


def _offending_lines(content: str) -> list[int]:
    ast = AST.build_from_javalang(build_ast_from_string(content))
    return ErClass().value(ast)

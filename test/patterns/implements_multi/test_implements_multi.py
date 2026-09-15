# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent

from aibolit.patterns.implements_multi.implements_multi import ImplementsMultiFinder
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast_from_string


def test_one_class_with_types() -> None:
    content = dedent(
        '''\
        class AnimatableSplit implements AnimatableValue {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_two_classes() -> None:
    content = dedent(
        '''\
        class AnimatableTransform implements ModifierContent, ContentModel {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_in_string() -> None:
    content = dedent(
        '''\
        class Dummy {
            String text = "implements Foo, Bar";
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_implements_with_parantheses() -> None:
    content = dedent(
        '''\
        class BaseKeyframe implements KeyframesWrapper<T> {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_implements_with_nested_parantheses() -> None:
    content = dedent(
        '''\
        class Configuration implements Iterable<Map.Entry<String, String>>, Writable {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_multi_classes() -> None:
    content = dedent(
        '''\
        class FillContent implements DrawingContent, AnimationListener, KeyPathElementContent {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_with_parantheses_multi() -> None:
    content = dedent(
        '''\
        class SumProcedure implements Procedure<Integer>, Function2<A, B, C>, Factory<SumProcedure> {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_with_parantheses_before() -> None:
    content = dedent(
        '''\
        class Dummy implements Procedure<Integer> {
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_implements_in_comments() -> None:
    content = dedent(
        '''\
        class Dummy {
            // implements Closeable, Configurable
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_implements_multi() -> None:
    content = dedent(
        '''\
        class OsSecureRandom extends Random implements Closeable, Configurable {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_three() -> None:
    content = dedent(
        '''\
        class RectangleContent implements AnimationListener, KeyPathElementContent, PathContent {
        }
        '''
    ).strip()
    assert _offending_lines(content) == [1]


def test_implements_many() -> None:
    content = dedent(
        '''\
        class SequenceFile {
            public static class Writer implements Closeable, Syncable {
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [2]


def _offending_lines(content: str) -> list[int]:
    ast = AST.build_from_javalang(build_ast_from_string(content))
    return ImplementsMultiFinder().value(ast)

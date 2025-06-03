# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent

import pytest

from aibolit.ast_framework import AST
from aibolit.metrics.npath.main import MvnFreeNPathMetric, NPathMetric
from aibolit.utils.ast_builder import build_ast_from_string


def testIncorrectFormat():
    with pytest.raises(Exception, match='PMDException'):
        file = 'test/metrics/npath/ooo.java'
        metric = NPathMetric(file)
        metric.value(True)


def testLowScore():
    file = 'test/metrics/npath/OtherClass.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 3
    assert res['data'][0]['file'] == file


def testHighScore():
    file = 'test/metrics/npath/Foo.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 200
    assert res['data'][0]['file'] == file


def testNonExistedFile():
    match = 'File test/metrics/npath/ooo1.java does not exist'
    with pytest.raises(Exception, match=match):
        file = 'test/metrics/npath/ooo1.java'
        metric = NPathMetric(file)
        metric.value(True)


def testMediumScore():
    file = 'test/metrics/npath/Complicated.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 12


class TestMvnFreeNPathMetric:
    def test_class_definition(self) -> None:
        content = dedent(
            """\
            class Dummy { }
            """
        ).strip()
        assert self._value(content) == 0

    def test_two_classes_definition(self) -> None:
        content = dedent(
            """\
            class First { }
            class Second { }
            """
        ).strip()
        assert self._value(content) == 0

    def test_one_if_statement(self) -> None:
        content = dedent(
            """\
            class WithOneIf {
                public void print(bool flag) {
                    if (flag) {
                        System.out.println("OK");
                    }
                }
            }
            """
        ).strip()
        assert self._value(content) == 2

    def test_one_if_else_statement(self) -> None:
        content = dedent(
            """\
            class WithOneIf {
                public void print(bool flag) {
                    if (flag) {
                        System.out.println("OK");
                    } else {
                        System.out.println("Not OK");
                    }
                }
            }
            """
        ).strip()
        assert self._value(content) == 2

    def test_if_with_inner_if_else(self) -> None:
        content = dedent(
            """\
            class WithOneIfWithInnerIfElse {
                public void print(bool flag, bool ok) {
                    if (flag) {
                        if (ok) {
                            System.out.println("OK");
                        } else {
                            System.out.println("Not OK");
                        }
                    }
                }
            }
            """
        ).strip()
        assert self._value(content) == 4

    def test_if_with_if_else_inside_outer_else(self) -> None:
        content = dedent(
            """\
            class WithOneIfWithIfElseInElseClause {
                public void print(bool flag, bool ok) {
                    if (flag) {
                        System.out.println("Flag is true");
                    } else {
                        if (ok) {
                            System.out.println("OK");
                        } else {
                            System.out.println("Not OK");
                        }
                    }
                }
            }
            """
        ).strip()
        assert self._value(content) == 4

    def test_complex_with_if_else_inside_if_else_blocks(self) -> None:
        content = dedent(
            """\
            class ComplexIfElse {
                public void checkValues(int a, int b) {
                    if (a > 0) {
                        if (b > 0) {
                            System.out.println("Both a and b are greater than 0");
                        } else {
                            System.out.println("a is greater than 0, but b is not");
                        }
                    } else {
                        if (b > 0) {
                            System.out.println("a is not greater than 0, but b is");
                        } else {
                            System.out.println("Neither a nor b is greater than 0");
                        }
                    }
                }
            }
            """
        ).strip()
        assert self._value(content) == 6

    def test_switch_simple(self):
        content = dedent(
            """\
            class Test {
                void foo(int x) {
                    switch (x) {
                        case 1: System.out.println("1"); break;
                        case 2: System.out.println("2"); break;
                        default: System.out.println("other");
                    }
                }
            }
            """,
        ).strip()
        assert self._value(content) == 3

    def test_switch_with_fallthrough(self):
        content = dedent(
            """\
            class Test {
                void foo(int x) {
                    switch (x) {
                        case 1:
                        case 2: System.out.println("1 or 2"); break;
                        case 3: System.out.println("3"); // fallthrough
                        case 4: System.out.println("3 or 4"); break;
                        default: System.out.println("other");
                    }
                }
            }
            """,
        )
        assert self._value(content) == 4

    def _value(self, content: str) -> int:
        return MvnFreeNPathMetric(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        ).value()

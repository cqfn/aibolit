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
            '''\
            class Dummy { }
            '''
        ).strip()
        assert self._value(content) == 0

    def test_two_classes_definition(self) -> None:
        content = dedent(
            '''\
            class First { }
            class Second { }
            '''
        ).strip()
        assert self._value(content) == 0

    def test_one_if_statement(self) -> None:
        content = dedent(
            '''\
            class WithOneIf {
                public void print(bool flag) {
                    if (flag) {
                        System.out.println("OK");
                    }
                }
            }
            '''
        ).strip()
        assert self._value(content) == 2

    def test_one_if_else_statement(self) -> None:
        content = dedent(
            '''\
            class WithOneIf {
                public void print(bool flag) {
                    if (flag) {
                        System.out.println("OK");
                    } else {
                        System.out.println("Not OK");
                    }
                }
            }
            '''
        ).strip()
        assert self._value(content) == 2

    def test_if_with_inner_if_else(self) -> None:
        content = dedent(
            '''\
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
            '''
        ).strip()
        assert self._value(content) == 3

    def test_if_with_if_else_inside_outer_else(self) -> None:
        content = dedent(
            '''\
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
            '''
        ).strip()
        assert self._value(content) == 3

    def test_complex_with_if_else_inside_if_else_blocks(self) -> None:
        """
        The four paths are:
        1. a > 0 and b > 0
        2. a > 0 and b <= 0
        3. a <= 0 and b > 0
        4. a <= 0 and b <= 0
        """
        content = dedent(
            '''\
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
            '''
        ).strip()
        assert self._value(content) == 4

    def test_complex_if_else_with_npath_complexity_of_5(self) -> None:
        content = dedent(
            '''\
            public class NPath5Example {
                public void checkValues(int a, int b) {
                    if (a > 0) { // Branch 1 (2 paths: true/false)
                        if (b > 0) { // Branch 2 (2 paths)
                            System.out.println("a > 0 and b > 0");
                        } else {
                            System.out.println("a > 0 but b <= 0");
                        }
                    } else { // Branch 3 (1 path, but 3 sub-paths)
                        if (b > 0) {
                            System.out.println("a <= 0 but b > 0");
                        } else if (b == 0) {
                            System.out.println("a <= 0 and b == 0");
                        } else {
                            System.out.println("a <= 0 and b < 0");
                        }
                    }
                }
            }
            '''
        ).strip()
        assert self._value(content) == 5

    def test_if_with_and_condition(self) -> None:
        content = '''
        class Test {
            void check(int a, int b) {
                if (a > 0 && b < 10) {
                    System.out.println("Valid");
                } else {
                    System.out.println("Invalid");
                }
            }
        }
        '''
        assert self._value(content) == 3

    def test_if_with_or_condition(self) -> None:
        content = '''
        class Test {
            void validate(int x, int y) {
                if (x == 0 || y == 0) {
                    System.out.println("Zero detected");
                } else {
                    System.out.println("No zeros");
                }
            }
        }
        '''
        assert self._value(content) == 3

    def test_switch_simple_with_default(self):
        content = dedent(
            '''\
            class Test {
                void foo(int x) {
                    switch (x) {
                        case 1: System.out.println("1"); break;
                        case 2: System.out.println("2"); break;
                        default: System.out.println("other");
                    }
                }
            }
            ''',
        ).strip()
        assert self._value(content) == 3

    def test_switch_empty(self):
        content = dedent(
            '''\
            class Test {
                void foo(int x) {
                    switch (x) {}
                }
            }
            ''',
        ).strip()
        assert self._value(content) == 1

    def test_switch_simple_without_default(self):
        content = dedent(
            '''\
            class Test {
                void foo(int x) {
                    switch (x) {
                        case 1: System.out.println("1"); break;
                        case 2: System.out.println("2"); break;
                    }
                }
            }
            ''',
        ).strip()
        assert self._value(content) == 2

    def test_switch_with_fallthrough(self):
        content = dedent(
            '''\
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
            ''',
        )
        assert self._value(content) == 4

    def test_nested_switch_statements(self) -> None:
        content = dedent(
            '''\
            class NestedSwitchStatements {
                public void process(int x, int y) {
                    switch (x) { // 1 path through case and 4 - default
                        case 1:
                            System.out.println("X=1");
                            break;
                        default:
                            switch (y) {
                                case 1: System.out.println("Y=1"); break;
                                case 2: System.out.println("Y=2"); break;
                                case 3: System.out.println("Y=3"); break;
                                default: System.out.println("Y=default"); break;
                            }
                    }
                }
            }
            '''
        ).strip()
        assert self._value(content) == 5

    def test_simple_for_loop(self) -> None:
        content = dedent('''
        class Test {
            void foo(int n) {
                for (int i = 0; i < n; i++) {
                    System.out.println(i);
                }
            }
        }
        ''').strip()
        assert self._value(content) == 2

    def test_for_with_and_condition(self) -> None:
        content = '''
        class Test {
            void foo(int n) {
                for (int i = 0; i < n && n > 0; i++) {
                    System.out.println(i);
                }
            }
        }
        '''
        assert self._value(content) == 3

    def test_for_with_or_condition(self) -> None:
        content = dedent(
            '''\
            class Test {
                void process(int a, int b) {
                    for (int i = 0; a > 0 || b < 10; i++) {
                        System.out.println("Processing: " + i);
                    }
                }
            }
            ''',
        ).strip()
        assert self._value(content) == 3

    def test_for_with_if_inside(self) -> None:
        content = dedent('''
        class Test {
            void bar(int n) {
                for (int i = 0; i < n; i++) {
                    if (i % 2 == 0) {
                        System.out.println("even");
                    }
                }
            }
        }
        ''').strip()
        assert self._value(content) == 3

    def test_nested_for_loops(self) -> None:
        content = dedent('''
        class Test {
            void matrix(int n) {
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        System.out.println(i * j);
                    }
                }
            }
        }
        ''').strip()
        assert self._value(content) == 3

    def test_for_with_switch(self) -> None:
        content = dedent('''
        class Test {
            void process(int[] data) {
                for (int x : data) {
                    switch (x) {
                        case 1: System.out.println("1");
                        case 2: System.out.println("2");
                        case 3: System.out.println("3");
                        default: break;
                    }
                }
            }
        }
        ''').strip()
        assert self._value(content) == 5

    def test_complex_for_with_multiple_constructs(self) -> None:
        content = dedent('''
        class Test {
            void analyze(int[] values) {
                for (int val : values) {
                    if (val > 0) {
                        switch (val) {
                            case 1: System.out.println("1");
                            default: break;
                        }
                    } else {
                        System.out.println("negative");
                    }
                }
            }
        }
        ''').strip()
        assert self._value(content) == 4

    def test_empty_infinite_for_loop(self) -> None:
        content = dedent('''
        class Test {
            void empty(int n) {
                for (;;);
            }
        }
        ''').strip()
        assert self._value(content) == 2

    def test_for_with_break_continue(self) -> None:
        content = dedent('''
        class Test {
            void search(int[] arr, int target) {
                for (int x : arr) {
                    if (x == target) {
                        break;
                    }
                    if (x < 0) {
                        continue;
                    }
                    System.out.println(x);
                }
            }
        }
        ''').strip()
        assert self._value(content) == 5

    def _value(self, content: str) -> int:
        return MvnFreeNPathMetric(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        ).value()

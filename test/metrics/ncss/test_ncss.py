# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import unittest
from textwrap import dedent

from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class TestNCSSMetric(unittest.TestCase):
    def testZeroScore(self):
        file = 'test/metrics/ncss/Empty.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 0)

    def testLowScore(self):
        file = 'test/metrics/ncss/Simple.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 2)

    def testBasicExample(self):
        file = 'test/metrics/ncss/BasicExample.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 13)

    def testSimpleExample(self):
        file = 'test/metrics/ncss/SimpleExample.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 18)

    def testSimpleExample2(self):
        file = 'test/metrics/ncss/SimpleExample2.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 19)

    def testChainedIfElse(self):
        file = 'test/metrics/ncss/ChainedIfElse.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 11)

    def testChainedIfElseWithTrailingElse(self):
        file = 'test/metrics/ncss/ChainedIfElseWithTrailingElse.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 12)

    def testFinallyBlock(self):
        file = 'test/metrics/ncss/FinallyBlock.java'
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 7)


def test_ncss_empty_class_declaration() -> None:
    content = dedent(
        '''\
        class Dummy {}
        '''
    ).strip()
    assert _nscc_metric_for(content) == 1


def test_ncss_class_with_one_attribute() -> None:
    content = dedent(
        '''\
        class Dummy {
          private int i;
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 2


def test_ncss_class_with_one_attribute_and_one_method() -> None:
    content = dedent(
        '''\
        class Dummy {
          private int i;
          private void run() {};
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 3


def test_ncss_class_with_one_attribute_and_two_methods() -> None:
    content = dedent(
        '''\
        class Dummy {
          private int i;
          private void runThis() {};
          private void runThat() {};
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 4


def test_ncss_class_with_try_catch() -> None:
    content = dedent(
        '''\
        class Dummy {
          private int numerator;
          public int divide(int denominator) {
            try {
                return this.numerator / this.denominator;
            }
            catch (Exception e) {
                throw e;
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 7


def test_ncss_class_with_try_catch_finally() -> None:
    content = dedent(
        '''\
        class Dummy {
          private int numerator;
          public int divide(int denominator) {
            try {
                return this.numerator / this.denominator;
            }
            catch (Exception e) {
                throw e;
            }
            finally {
                System.out.println("Tried to divide");
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 9


def test_ncss_class_with_while_loop() -> None:
    content = dedent(
        '''\
        class Dummy {
          private void printStuff() {
            while(1) {
                System.out.println("Hello");
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 4


def test_ncss_class_with_if_statement() -> None:
    content = dedent(
        '''\
        class Dummy {
          private void printStuff(bool ok) {
            if (ok) {
              System.out.println("OK");
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 4


def test_ncss_class_with_if_else_statements() -> None:
    content = dedent(
        '''\
        class Dummy {
          private void printStuff(bool ok) {
            if (ok) {
              System.out.println("OK");
            } else {
              System.out.println("Not OK");
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 6


def test_ncss_class_with_if_else_if_else_statements() -> None:
    content = dedent(
        '''\
        class Dummy {
          private void printStuff(int value) {
            if (value == 1) {
              System.out.println("OK");
            } else if (value == 2) {
              System.out.println("Not OK");
            }
            else {
              throw new Exception('Unexpected value');
            }
          };
        }
        '''
    ).strip()
    assert _nscc_metric_for(content) == 8


def _nscc_metric_for(content: str) -> int:
    return NCSSMetric().value(
        AST.build_from_javalang(
            build_ast_from_string(content),
        ),
    )

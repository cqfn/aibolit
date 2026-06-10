# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from unittest import TestCase
from pathlib import Path
from textwrap import dedent

from aibolit.metrics.cc.main import CCMetric
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import read_text_with_autodetected_encoding, build_ast_from_string


class CCTestCase(TestCase):
    def test_complicated_example(self):
        self.assertEqual(self._cc_metric_for_file('Complicated.java'), 12)

    def test_other_class_example(self):
        self.assertEqual(self._cc_metric_for_file('OtherClass.java'), 3)

    def test_empty_method(self):
        content = dedent(
            '''\
            class Dummy {
              private void empty() {}
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 1)

    def test_simple_if_statement(self):
        content = dedent(
            '''\
            class Dummy {
              private void test(boolean condition) {
                if (condition) {
                  System.out.println("true");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_if_else_statement(self):
        content = dedent(
            '''\
            class Dummy {
              private void test(boolean condition) {
                if (condition) {
                  System.out.println("true");
                } else {
                  System.out.println("false");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_while_loop(self):
        content = dedent(
            '''\
            class Dummy {
              private void test(int n) {
                while (n > 0) {
                  n--;
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_for_loop(self):
        content = dedent(
            '''\
            class Dummy {
              private void test() {
                for (int i = 0; i < 10; i++) {
                  System.out.println(i);
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_switch_statement(self):
        content = dedent(
            '''\
            class Dummy {
              private void test(int value) {
                switch (value) {
                  case 1:
                    System.out.println("one");
                    break;
                  case 2:
                    System.out.println("two");
                    break;
                  default:
                    System.out.println("other");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 6)

    def test_try_catch(self):
        content = dedent(
            '''\
            class Dummy {
              private void test() {
                try {
                  System.out.println("try");
                } catch (Exception e) {
                  System.out.println("catch");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_ternary_operator(self):
        content = dedent(
            '''\
            class Dummy {
              private String test(boolean condition) {
                return condition ? "true" : "false";
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def test_boolean_operators(self):
        content = dedent(
            '''\
            class Dummy {
              private void test(boolean a, boolean b, boolean c) {
                if (a && b || c) {
                  System.out.println("complex condition");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 4)

    def test_multiple_methods(self):
        content = dedent(
            '''\
            class Dummy {
              private void method1() {
                if (true) {
                  System.out.println("method1");
                }
              }

              private void method2() {
                for (int i = 0; i < 5; i++) {
                  System.out.println("method2");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 4)

    def test_multiple_nested_statements(self):
        content = dedent(
            '''\
            class Dummy {
              void test() {                     // CC = 11
                int x = 0, y = 2;
                boolean a = false, b = true;
                if (a && (y == 1 ? b : true)) { // +3
                  if (y == x) {                 // +1
                    while (true) {              // +1
                      if (x++ < 20) {           // +1
                        break;                  // +1
                      }
                    }
                  } else if (y == 1 && !b) {    // +2
                    x = a ? y : x;              // +1
                  } else {
                    x = 2;
                  }
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 11)

    def test_multiple_boolean_operators(self):
        content = dedent(
            '''\
            class Dummy {
              void test() {                       // CC = 8
                int x=0, y=1;
                boolean a, b;
                if (x > 2 || y < 4) {             // +2
                  while (x++ < 10 && !(y++ < 0)); // +2
                } else if (a && b || x < 4) {     // +3
                  return;
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 8)

    def test_constructor_also_counted(self):
        content = dedent(
            '''\
            class Dummy {
              Dummy() {
                if (true) {
                  System.out.println("constructor");
                }
              }
            }
            '''
        ).strip()
        self.assertEqual(self._cc_metric_for(content), 2)

    def _cc_metric_for_file(self, filename: str) -> int:
        path = Path(__file__).absolute().parent / filename
        return self._cc_metric_for(read_text_with_autodetected_encoding(str(path)))

    def _cc_metric_for(self, content: str) -> int:
        return CCMetric().value(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        )

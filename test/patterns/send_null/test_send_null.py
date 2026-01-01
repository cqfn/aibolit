# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.send_null.send_null import SendNull
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class SendNullTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_one_send(self):
        filepath = self.current_directory / 'BaseKeyframeAnimation.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [149])

    def test_multi_level_invocation(self):
        filepath = self.current_directory / 'Configuration.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(
            lines,
            [382, 445, 552, 641, 659, 833, 869, 1365, 2396, 2877, 2991, 3083, 3495, 3761, 3858]
        )

    def test_no_null_methods(self):
        filepath = self.current_directory / 'FillContent.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple_invocation(self):
        filepath = self.current_directory / 'FJIterateTest.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [489])

    def test_constructor_send_null(self):
        filepath = self.current_directory / 'Constructor.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [8, 17, 18, 19, 20, 21])

    def test_super_in_constructor_with_ternary_operator(self):
        filepath = self.current_directory / 'AclPermissionParam.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [49, 53])

    def test_this_with_ternary_operator(self):
        filepath = self.current_directory / 'AddOp.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [31, 35])

    def test_super_in_constructor_with_method_inv(self):
        filepath = self.current_directory / 'ByteArrayMultipartFileEditor.java'
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = SendNull()
        lines = pattern.value(ast)
        self.assertEqual(lines, [51])


def test_pass_null_as_the_only_parameter_into_another_private_method() -> None:
    content = dedent(
        '''\
        class Dummy {
          private byte tmp;
          private doSomething(byte value) {}
          private passNullIntoAnotherMethod() {
            doSomething(null);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [5]


def test_pass_null_into_method_for_poorly_formatted_file() -> None:
    content = dedent(
        '''\
        class Dummy {
            private byte tmp;
          private doSomething( byte value  ) {}
             private passNullIntoAnotherMethod(
          ) {
            doSomething(

            null);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [8]


def test_pass_null_as_the_first_parameter_into_another_private_method() -> None:
    content = dedent(
        '''\
        class Dummy {
          private byte tmp;
          private doSomething(byte value, int number) {}
          private passNullIntoAnotherMethod() {
            doSomething(null, 1);
          }
        }
        '''
    ).strip()
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = SendNull()
    assert pattern.value(ast) == [5]


def test_pass_null_as_the_first_parameter_into_another_private_method_on_newline() -> None:
    content = dedent(
        '''\
        class Dummy {
          private byte tmp;
          private doSomething(byte value, int number) {}
          private passNullIntoAnotherMethod() {
            doSomething(
              null,
              1);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [6]


def test_pass_null_as_the_second_parameter_into_another_private_method_on_newline() -> None:
    content = dedent(
        '''\
        class Dummy {
          private byte tmp;
          private doSomething(int number, short value) {}
          private passNullIntoAnotherMethod() {
            doSomething(1,
              null);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [6]


def test_pass_null_as_parameter_into_another_private_method() -> None:
    content = dedent(
        '''\
        class Dummy {
          private doSomething(byte value) {}
          private passNullIntoAnotherMethod() {
            doSomething(null);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [4]


def test_pass_null_as_parameter_into_another_public_method() -> None:
    content = dedent(
        '''\
        class Dummy {
          public doSomething(byte value) {}
          public passNullIntoAnotherMethod() {
            doSomething(null);
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [4]


def test_pass_null_into_hashmap_in_for_loop() -> None:
    content = dedent(
        '''\
        class Dummy {
          HashMap<String, String> map = new HashMap<String, String>();
          public passNullIntoHashMap() {
            for (int i = 0; i < 5; i++) {
              map.put("SomeText", null);
            }
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [5]


def test_pass_null_into_array_list() -> None:
    content = dedent(
        '''\
        class Dummy {
          ArrayList<String> cars = new ArrayList<String>();
          public passNullIntoArrayList() {
            cars.add("Ferrari");
            cars.add("Toyota");
            cars.add(null);
            cars.add("Lada");
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [6]


def test_pass_null_as_the_only_parameter_into_another_ctor() -> None:
    content = dedent(
        '''\
        class Caller {
          public callAnotherClassCtorWithNull() {
            Other(null);
          }
        }

        class Other {
          private byte value;
          public Other(byte value) {
            this.value = value;
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_pass_null_as_the_first_parameter_into_another_ctor() -> None:
    content = dedent(
        '''\
        class Caller {
          public callAnotherClassCtorWithNull() {
            Other(null, 1);
          }
        }

        class Other {
          private int number;
          private short value;
          public Other(int number, short value) {
            this.number = number;
            this.value = value;
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_pass_null_as_the_second_parameter_into_another_ctor() -> None:
    content = dedent(
        '''\
        class Caller {
          public callAnotherClassCtorWithNull() {
            Other(0, null);
          }
        }

        class Other {
          private int number;
          private byte value;
          public Other(int number, byte value) {
            this.number = number;
            this.value = value;
          }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_null_in_ternary_expression_comparison_with_class_creator() -> None:
    content = dedent(
        '''\
        public class Dummy {
            transient volatile Set<Integer> keySet = null;
            public Set<Integer> keySet() {
                Set<Integer> ks = keySet;
                return (ks != null ? ks : (keySet = new KeySet()));
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def _offending_lines(content: str) -> list[int]:
    """Return a list of lines offending SendNull pattern."""
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = SendNull()
    return pattern.value(ast)

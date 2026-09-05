# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent

from aibolit.patterns.send_null.send_null import SendNull
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast_from_string


def test_one_send() -> None:
    content = dedent(
        '''\
        class BaseKeyframeAnimation {
            public void setValueCallback(Object valueCallback) {
                this.valueCallback.setAnimation(null);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_multi_level_invocation() -> None:
    content = dedent(
        '''\
        class Configuration {
            private String getWarningMessage(String key) {
                return getWarningMessage(key, null);
            }
            public void addDeprecation(String key, String[] newKeys) {
                addDeprecation(key, newKeys, null);
            }
            public void set(String name, String value) {
                set(name, value, null);
            }
            public void writeXml(Writer out) {
                writeXml(null, out);
            }
            public void register() {
                REGISTRY.put(this, null);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3, 6, 9, 12, 15]


def test_no_null_methods() -> None:
    content = dedent(
        '''\
        class FillContent {
            public void draw() {
                paint.setColor(color);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_simple_invocation() -> None:
    content = dedent(
        '''\
        class FJIterateTest {
            public void groupByNulls() {
                FJIterate.groupBy(null, null, 1);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_constructor_send_null() -> None:
    content = dedent(
        '''\
        class CompressionOption {
            CompressionOption(CompressionType value) {
                this(value, null);
            }
            CompressionOption(CompressionType value, CompressionCodec codec) {
                this.value = value;
            }
            CompressionType getValue() {
                a.method_call(2, b.method_call(null));
                a.method_call().method_call(b).method_call(null);
                doSomething(myString = ((myString != 5) ? null : myString), obj);
                doSomething(myString = ((myString != 5) ? myString.toLowerCase() : null), obj);
                new Object(null);
                return value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3, 9, 10, 11, 12, 13]


def test_super_in_constructor_with_ternary_operator() -> None:
    content = dedent(
        '''\
        class AclPermissionParam extends StringParam {
            public AclPermissionParam(final String str) {
                super(DOMAIN, str == null || str.equals(DEFAULT) ? null : str);
            }
            public AclPermissionParam(List acl) {
                super(DOMAIN, parseAclSpec(acl).equals(DEFAULT) ? null : parseAclSpec(acl));
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3, 6]


def test_this_with_ternary_operator() -> None:
    content = dedent(
        '''\
        class AddOp {
            public AddOp(INDArray first, INDArray second, INDArray result) {
                this(new INDArray[]{first, second}, result == null ? null : new INDArray[]{result});
            }
            public AddOp(INDArray x, INDArray y) {
                this(new INDArray[]{x, y}, null);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3, 6]


def test_super_in_constructor_with_method_inv() -> None:
    content = dedent(
        '''\
        class ByteArrayMultipartFileEditor {
            public void setValue(Object value) {
                super.setValue(value != null ? value.toString().getBytes() : null);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


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

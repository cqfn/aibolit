# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

from textwrap import dedent

from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast_from_string


def test_setSomething_is_not_a_setter_unless_sets_value_to_attribute() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            private int attr;
            public void setSunset() {
                System.out.println("This is not a setter");
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_settle_is_not_a_setter_even_though_has_one_argument() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            public void settle(String place) {
                System.out.println("Let us settle here:" + place);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_settings_is_not_a_setter_as_it_calls_method() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            public void settings(Difficulty difficulty, Resolution resolution) {
                this.gameSettings.apply(difficulty, resolution);
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_update_attribute_in_method_starting_with_set_is_not_a_setter() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            private int coupling;
            public void setMeFree() {
                this.coupling = 0;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_update_flag_with_boolean_value_is_not_a_setter() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            private bool isFree;
            public void setMeFree() {
                isFree = true;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_fake_setter_when_defined_inplace() -> None:
    content = dedent(
        '''\
        class ProgramUserDataDB extends DomainObjectAdapterDB implements ProgramUserData {
            private final ChangeManager changeMgr = new ChangeManagerAdapter() {
                @Override
                public void setPropertyChanged(String propertyName, Address codeUnitAddr) {
                    changed = true;
                    program.userDataChanged(propertyName, codeUnitAddr);
                }
            };
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_setka_is_not_a_setter_even_though_starts_with_set() -> None:
    content = dedent(
        '''\
        class FakeSetterClass {
            public void setka() {
                System.out.println("Not a setter");
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def test_simple_setter() -> None:
    content = dedent(
        '''\
        class SimpleSetterClass {
            private int attr;
            public void setAttr(int value) {
                this.attr = value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_simple_setter_on_one_line() -> None:
    content = dedent(
        '''\
        class SimpleSetterClass {
            private int attr;
            public void setAttr(int value) { this.attr = value; }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_setter_without_referencing_this() -> None:
    content = dedent(
        '''\
        class SimpleSetterClass {
            private int attr;
            public void setAttr(int value) {
                attr = value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_setter_with_side_effect() -> None:
    content = dedent(
        '''\
        class SetterWithSideEffectClass {
            private int attr;
            public void setAttr(int value) {
                System.out.println("Side effect");
                this.attr = value;
                System.out.println("Another side effect");
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [3]


def test_setter_with_annotation() -> None:
    content = dedent(
        '''\
        class SimpleSetterClassWithAnnotation {
            private int attr;
            @VisibleForTesting
            public void setAttr(int value) {
                this.attr = value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [4]


def test_setter_in_inner_class() -> None:
    content = dedent(
        '''\
        class ClassWithInnerSetterClass {
            class InnerSetterClass {
                private int attr;
                public void setAttr(int value) {
                    attr = value;
                }
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [4]


def test_two_setters() -> None:
    content = dedent(
        '''\
        class ClassWithTwoSetters {
            private int tomato;
            private double potato;
            public void setTomato(int value) {
                tomato = value;
            }
            public void method() {
                System.out.println("Do something");
            }
            public void setPotato(int value) {
                this.potato = value;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == [4, 10]


def test_update_attribute_in_method_is_not_a_setter() -> None:
    content = dedent(
        '''\
        class ClassWithoutSetters {
            private int attr;
            public void multiply(int multiplier) {
                this.attr = this.attr * multiplier;
            }
        }
        '''
    ).strip()
    assert _offending_lines(content) == []


def _offending_lines(content: str) -> list[int]:
    """Return a list of lines matching ClassicSetter pattern."""
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = ClassicSetter()
    return pattern.value(ast)

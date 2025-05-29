# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from textwrap import dedent
from unittest import TestCase

import pytest

from aibolit.patterns.classic_setter.classic_setter import ClassicSetter
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


class SetterTestCase(TestCase):
    current_directory = Path(__file__).absolute().parent

    def test_four_setter_patterns(self):
        filepath = self.current_directory / "Configuration.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines,
                         [905, 909, 1239, 1243, 1364, 1542, 1615, 1644, 1673,
                          1706, 1715, 1726, 1804, 1973, 2023, 2339,
                          2510, 3786, 3822])

    def test_another_setter_patterns(self):
        filepath = self.current_directory / "SequenceFile.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = ClassicSetter()
        lines = pattern.value(ast)
        self.assertEqual(lines, [262, 747, 2852, 2858, 2864, 3130])


@pytest.mark.xfail(reason='Wrong implementation')
def test_setSomething_is_not_a_setter_unless_sets_value_to_attribute() -> None:
    # TODO #777:15min/DEV It is necessary to handle case of a fake setter.
    #  When the method starts with `set`,
    #  but does not assign to the attribute is not a setter.
    #  Once the implementation is updated,
    #  remove `xfail` mark above this test definition.
    content = dedent(
        """\
        class FakeSetterClass {
            private int attr;
            public void setSunset() {
                System.out.println("This is not a setter");
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


@pytest.mark.xfail(reason='Incomplete implementation')
def test_settle_is_not_a_setter_even_though_has_one_argument() -> None:
    # TODO #777:15min/DEV It is necessary to handle case of a fake setter.
    #  When the method starts with `set` and has one input parameter,
    #  but does not assign to the attribute is not a setter.
    #  Once the implementation is updated,
    #  remove `xfail` mark above this test definition.
    content = dedent(
        """\
        class FakeSetterClass {
            public void settle(String place) {
                System.out.println("Let us settle here:" + place);
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


@pytest.mark.xfail(reason='Incomplete implementation')
def test_settings_is_not_a_setter_as_it_calls_method() -> None:
    # TODO #777:15min/DEV It is necessary to handle case of a fake setter.
    #  When the method starts with `set` and calls an external method,
    #  without assigning to the attribute, is not a setter.
    #  Once the implementation is updated,
    #  remove `xfail` mark above this test definition.
    content = dedent(
        """\
        class FakeSetterClass {
            public void settings(Difficulty difficulty, Resolution resolution) {
                this.gameSettings.apply(difficulty, resolution);
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


@pytest.mark.xfail(reason='Incomplete implementation')
def test_update_attribute_in_method_starting_with_set_is_not_a_setter() -> None:
    # TODO #777:15min/DEV It is necessary to handle case of a fake setter.
    #  When the method starts with `set`, changes the value of the attribute,
    #  but does not assign the input parameter to the attribute,
    #  is not a setter.
    #  Once the implementation is updated,
    #  remove `xfail` mark above this test definition.
    content = dedent(
        """\
        class FakeSetterClass {
            private int coupling;
            public void setMeFree() {
                this.coupling = 0;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


@pytest.mark.xfail(reason='Incomplete implementation')
def test_setka_is_not_a_setter_even_though_starts_with_set() -> None:
    # TODO #777:15min/DEV It is necessary to handle case of a fake setter.
    #  When the method starts with `set`, followed by a non-capital letter,
    #  without even assigning a value to the attribute,
    #  is not a setter.
    #  Once the implementation is updated,
    #  remove `xfail` mark above this test definition.
    content = dedent(
        """\
        class FakeSetterClass {
            public void setka() {
                System.out.println("Not a setter");
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


def test_simple_setter() -> None:
    content = dedent(
        """\
        class SimpleSetterClass {
            private int attr;
            public void setAttr(int value) {
                this.attr = value;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == [3]


def test_setter_without_referencing_this() -> None:
    content = dedent(
        """\
        class SimpleSetterClass {
            private int attr;
            public void setAttr(int value) {
                attr = value;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == [3]


def test_setter_with_annotation() -> None:
    content = dedent(
        """\
        class SimpleSetterClassWithAnnotation {
            private int attr;
            @VisibleForTesting
            public void setAttr(int value) {
                this.attr = value;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == [4]


def test_setter_in_inner_class() -> None:
    content = dedent(
        """\
        class ClassWithInnerSetterClass {
            class InnerSetterClass {
                private int attr;
                public void setAttr(int value) {
                    attr = value;
                }
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == [4]


def test_two_setters() -> None:
    content = dedent(
        """\
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
        """
    ).strip()
    assert _offending_lines(content) == [4, 10]


def test_update_attribute_in_method_is_not_a_setter() -> None:
    content = dedent(
        """\
        class ClassWithoutSetters {
            private int attr;
            public void multiply(int multiplier) {
                this.attr = this.attr * multiplier;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


def _offending_lines(content: str) -> list[int]:
    """Return a list of lines matching ClassicSetter pattern."""
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = ClassicSetter()
    return pattern.value(ast)

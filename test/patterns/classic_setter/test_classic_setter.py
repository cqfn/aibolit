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


def test_update_attribute_in_method_is_not_a_setter() -> None:
    content = dedent(
        """\
        class SimpleSetterClass {
            private int attr;
            public void multiply(int multiplier) {
                this.attr = this.attr * multiplier;
            }
        }
        """
    ).strip()
    assert _offending_lines(content) == []


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


def _offending_lines(content: str) -> list[int]:
    """Return a list of lines matching ClassicSetter pattern."""
    ast = AST.build_from_javalang(build_ast_from_string(content))
    pattern = ClassicSetter()
    return pattern.value(ast)

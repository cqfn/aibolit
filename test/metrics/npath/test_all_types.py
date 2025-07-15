# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
import pathlib

import pytest

from aibolit.ast_framework import AST
from aibolit.metrics.npath.main import MvnFreeNPathMetric, NPathMetric
from aibolit.utils.ast_builder import build_ast, build_ast_from_string


def testIncorrectFormat():
    with pytest.raises(Exception, match='PMDException'):
        file = 'test/metrics/npath/javacode/ooo.java'
        metric = NPathMetric(file)
        metric.value(True)


def testLowScore():
    file = 'test/metrics/npath/javacode/OtherClass.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 3
    assert res['data'][0]['file'] == file


def testHighScore():
    file = 'test/metrics/npath/javacode/EvenMoreComplicated.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 200
    assert res['data'][0]['file'] == file


def testNonExistedFile():
    match = 'File test/metrics/npath/javacode/ooo1.java does not exist'
    with pytest.raises(Exception, match=match):
        file = 'test/metrics/npath/javacode/ooo1.java'
        metric = NPathMetric(file)
        metric.value(True)


def testMediumScore():
    file = 'test/metrics/npath/javacode/Complicated.java'
    metric = NPathMetric(file)
    res = metric.value(True)
    assert res['data'][0]['complexity'] == 12


class TestMvnFreeNPathMetric:
    def test_class_definition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ClassDefinition.java')) == 0

    def test_two_classes_definition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/TwoClassesDefinition.java')) == 0

    def test_one_if_statement(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/OneIfStatement.java')) == 2

    def test_one_if_else_statement(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/OneIfElseStatement.java')) == 2

    def test_if_with_inner_if_else(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/IfWithInnerIfElse.java')) == 3

    def test_if_with_if_else_inside_outer_else(self) -> None:
        file = 'javacode/IfWithIfElseInsideOuterElse.java'
        assert self._value_from_filepath(self._filepath(file)) == 3

    def test_complex_with_if_else_inside_if_else_blocks(self) -> None:
        file = 'javacode/ComplexWithIfElseInsideIfElseBlocks.java'
        assert self._value_from_filepath(self._filepath(file)) == 4

    def test_complex_if_else_with_npath_complexity_of_5(self) -> None:
        file = 'javacode/ComplexIfElseWithNPathComplexityOf5.java'
        assert self._value_from_filepath(self._filepath(file)) == 5

    def test_if_with_and_condition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/IfWithAndCondition.java')) == 3

    def test_if_with_or_condition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/IfWithOrCondition.java')) == 3

    def test_switch_simple_with_default(self) -> None:
        file = 'javacode/SwitchSimpleWithDefault.java'
        assert self._value_from_filepath(self._filepath(file)) == 3

    def test_test_switch_empty(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/TestSwitchEmpty.java')) == 2

    def test_switch_simple_without_default(self) -> None:
        file = 'javacode/SwitchSimpleWithoutDefault.java'
        assert self._value_from_filepath(self._filepath(file)) == 3

    def test_switch_with_fallthrough(self) -> None:
        file = 'javacode/SwitchWithFallthrough.java'
        assert self._value_from_filepath(self._filepath(file)) == 5

    def test_nested_switch_statements(self) -> None:
        file = 'javacode/NestedSwitchStatements.java'
        assert self._value_from_filepath(self._filepath(file)) == 5

    def test_simple_for_loop(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/SimpleForLoop.java')) == 2

    def test_for_with_and_condition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ForWithAndCondition.java')) == 3

    def test_for_with_or_condition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ForWithOrCondition.java')) == 3

    def test_for_with_if_inside(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ForWithIfInside.java')) == 3

    def test_nested_for_loops(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/NestedForLoops.java')) == 3

    def test_for_with_switch(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ForWithSwitch.java')) == 5

    def test_comlpex_for_with_multiple_constructs(self) -> None:
        file = 'javacode/ComlpexForWithMultipleConstructs.java'
        assert self._value_from_filepath(self._filepath(file)) == 4

    def test_empty_infinite_for_loop(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/EmptyInfiniteForLoop.java')) == 2

    def test_for_with_break_continue(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/ForWithBreakContinue.java')) == 5

    def test_simple_while_loops(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/SimpleWhileLoops.java')) == 2

    def test_while_with_if(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/WhileWithIf.java')) == 3

    def test_while_with_or_condition(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/WhileWithOrCondition.java')) == 6

    def test_while_with_and_condition(self) -> None:
        file = 'javacode/WhileWithAndCondition.java'
        assert self._value_from_filepath(self._filepath(file)) == 3

    def test_while_with_break(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/WhileWithBreak.java')) == 3

    def test_empty_while_loop(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/EmptyWhileLoop.java')) == 2

    def test_nested_while_loops(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/NestedWhileLoops.java')) == 3

    def test_complicated(self) -> None:
        assert self._value_from_filepath(self._filepath('javacode/Complicated.java')) == 12

    def test_even_more_complicated(self) -> None:
        file = 'javacode/EvenMoreComplicated.java'
        assert self._value_from_filepath(self._filepath(file)) == 288

    def _filepath(self, basename: str) -> pathlib.Path:
        return pathlib.Path(__file__).parent / basename

    def _value(self, content: str) -> int:
        return self._metric(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        )

    def _value_from_filepath(self, filepath: str | os.PathLike) -> int:
        return self._metric(
            AST.build_from_javalang(
                build_ast(filepath),
            ),
        )

    def _metric(self, ast: AST) -> int:
        return MvnFreeNPathMetric(ast).value()

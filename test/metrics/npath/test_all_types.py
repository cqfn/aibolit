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

    def _value(self, content: str) -> int:
        return MvnFreeNPathMetric(
            AST.build_from_javalang(
                build_ast_from_string(content),
            ),
        ).value()

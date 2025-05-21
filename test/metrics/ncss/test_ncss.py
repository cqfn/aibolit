# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import unittest

from aibolit.metrics.ncss.ncss import NCSSMetric
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class TestNCSSMetric(unittest.TestCase):
    def testZeroScore(self):
        file = "test/metrics/ncss/Empty.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 0)

    def testLowScore(self):
        file = "test/metrics/ncss/Simple.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 2)

    def testBasicExample(self):
        file = "test/metrics/ncss/BasicExample.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 13)

    def testSimpleExample(self):
        file = "test/metrics/ncss/SimpleExample.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 18)

    def testSimpleExample2(self):
        file = "test/metrics/ncss/SimpleExample2.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 19)

    def testChainedIfElse(self):
        file = "test/metrics/ncss/ChainedIfElse.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 11)

    def testChainedIfElseWithTrailingElse(self):
        file = "test/metrics/ncss/ChainedIfElseWithTrailingElse.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 12)

    def testFinallyBlock(self):
        file = "test/metrics/ncss/FinallyBlock.java"
        ast = AST.build_from_javalang(build_ast(file))
        metric = NCSSMetric()
        res = metric.value(ast)
        self.assertEqual(res, 7)

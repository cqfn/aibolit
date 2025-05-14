# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase

from aibolit.patterns.redundant_catch.redundant_catch import RedundantCatch
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class RedundantCatchTestCase(TestCase):
    def test_simple(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/Simple.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_both_catches(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/BothCatches.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_fake(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/TrickyFake.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_try_inside_anonymous(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/TryInsideAnonymous.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [9, 17])

    def test_multiple_catch(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/MultipleCatch.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_sequential_catch(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/SequentialCatch.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [6])

    def test_sequential_catch_try(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/SequentialCatchTry.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [6, 13])

    def test_try_inside_catch(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/TryInsideCatch.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [10])

    def test_try_inside_finally(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/TryInsideFinally.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [11])

    def test_try_inside_try(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/TryInsideTry.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [8])

    def test_catch_with_functions(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/CatchWithFunctions.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [9])

    def test_catch_with_similar_name(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/NotThrow.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [258])

    def test_try_without_throws(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/ExcelReader.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_try_in_constructor(self):
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/ExcelAnalyserImpl.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [46])

    def test_fake_try_in_lambda(self):
        """
        If function has throws, the pattern shouldn't be recognized
        if the same exception is caught in anonymous lambda
        """
        pattern = RedundantCatch()
        filepath = os.path.dirname(os.path.realpath(__file__)) + "/Cache.java"
        ast = AST.build_from_javalang(build_ast(filepath))
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

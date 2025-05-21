# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

from pathlib import Path
from unittest import TestCase

from aibolit.patterns.hybrid_constructor.hybrid_constructor import HybridConstructor
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class HybridConstructorTestCase(TestCase):
    cur_dir = Path(__file__).absolute().parent

    def test_several(self):
        filepath = Path(self.cur_dir, "several.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7, 13, 23])

    def test_simple2(self):
        filepath = Path(self.cur_dir, "init_block.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple22(self):
        filepath = Path(self.cur_dir, "init_static_block.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple3(self):
        filepath = Path(self.cur_dir, "autocloseable.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [7, 17, 34])

    def test_simple5(self):
        filepath = Path(self.cur_dir, "one_line_usage.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_simple6(self):
        filepath = Path(self.cur_dir, "super.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [15])

    def test_simple7(self):
        filepath = Path(self.cur_dir, "holy_moly_constructor.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [50])

    def test_simple9(self):
        filepath = Path(self.cur_dir, "super_this.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [18, 28, 54, 65, 79, 90, 104])

    def test_simple10(self):
        filepath = Path(self.cur_dir, "BookmarkEditCmd.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple11(self):
        filepath = Path(self.cur_dir, "ChainedBuffer.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple12(self):
        filepath = Path(self.cur_dir, "CliMethodExtraSections.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple13(self):
        filepath = Path(self.cur_dir, "LengthStringOrdinalSet.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple14(self):
        filepath = Path(self.cur_dir, "LoaderInfoHeader.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

    def test_simple15(self):
        filepath = Path(self.cur_dir, "OmfModuleEnd.java")
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = HybridConstructor()
        lines = pattern.value(ast)
        self.assertEqual(lines, [])

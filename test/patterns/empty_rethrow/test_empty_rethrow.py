# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
from unittest import TestCase
from pathlib import Path

from aibolit.patterns.empty_rethrow.empty_rethrow import EmptyRethrow
from aibolit.ast_framework import AST
from aibolit.utils.ast_builder import build_ast


class EmptyRethrowTestCase(TestCase):
    current_directory = Path(os.path.realpath(__file__)).parent

    def test_empty(self):
        filepath = str(Path(self.current_directory, "Empty.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_anonymous(self):
        filepath = str(Path(self.current_directory, "Anonymous.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [22, 28])

    def test_both_catches(self):
        filepath = str(Path(self.current_directory, "BothCatches.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9, 11])

    def test_instance_different_methods(self):
        filepath = str(Path(self.current_directory, "MultipleCatch.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9])

    def test_sequential_catch(self):
        filepath = str(Path(self.current_directory, "SequentialCatch.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9, 11])

    def test_sequential_catch_try(self):
        filepath = str(Path(self.current_directory, "SequentialCatchTry.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9, 11, 16, 18])

    def test_simple(self):
        filepath = str(Path(self.current_directory, "Simple.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9])

    def test_tricky_fake(self):
        filepath = str(Path(self.current_directory, "TrickyFake.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_try_inside_catch(self):
        filepath = str(Path(self.current_directory, "TryInsideCatch.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [13])

    def test_try_inside_finally(self):
        filepath = str(Path(self.current_directory, "TryInsideFinally.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [9, 15])

    def test_try_inside_try(self):
        filepath = str(Path(self.current_directory, "TryInsideTry.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [13, 20])

    def test_catch_with_functions(self):
        filepath = str(Path(self.current_directory, "CatchWithFunctions.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [16])

    def test_catch_with_if(self):
        filepath = str(Path(self.current_directory, "CatchWithIf.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [17])

    def test_chained_exceptions1(self):
        filepath = str(Path(self.current_directory, "DataBaseNavigator.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_chained_exceptions2(self):
        filepath = str(Path(self.current_directory, "ConfigImportWizardPageDbvis.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_chained_exceptions3(self):
        filepath = str(Path(self.current_directory, "DatabaseNavigatorSourceContainer.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_try_without_catch(self):
        filepath = str(Path(self.current_directory, "ConcurrentDiskUtil.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

    def test_throw_with_cast(self):
        filepath = str(Path(self.current_directory, "CommonRdbmsReader.java"))
        ast = AST.build_from_javalang(build_ast(filepath))
        pattern = EmptyRethrow()
        self.assertEqual(pattern.value(ast), [])

# SPDX-FileCopyrightText: Copyright (c) 2019-2026 Aibolit
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from unittest import TestCase

from aibolit.ast_framework import AST
from aibolit.patterns.non_final_argument.non_final_argument import NonFinalArgument
from aibolit.utils.ast_builder import build_ast


class NonFinalArgumentTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_argument_in_ctor(self):
        self.assertEqual(
            NonFinalArgument().value(self._ast('NonFinalArgumentCtor.java')), [10]
        )

    def test_find_non_final_argument_in_method(self):
        self.assertEqual(
            NonFinalArgument().value(self._ast('NonFinalArgumentMethod.java')), [14]
        )

    def _ast(self, filename):
        return AST.build_from_javalang(build_ast(Path(self.dir_path, filename)))

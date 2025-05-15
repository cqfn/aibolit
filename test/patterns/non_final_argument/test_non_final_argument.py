# SPDX-FileCopyrightText: Copyright (c) 2019-2025 Aibolit
# SPDX-License-Identifier: MIT

import os
import unittest
from pathlib import Path
from unittest import TestCase

from aibolit.patterns.non_final_argument.non_final_argument import NonFinalArgument


@unittest.skip("Not implemented")
class NonFinalArgumentTestCase(TestCase):
    dir_path = Path(os.path.realpath(__file__)).parent

    def test_find_non_final_argument_in_ctor(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, "NonFinalArgumentCtor.java")), [7]
        )

    def test_find_non_final_argument_in_method(self):
        self.assertEqual(
            NonFinalArgument().value(Path(self.dir_path, "NonFinalArgumentMethod.java")), [11]
        )
